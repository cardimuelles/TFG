import sys,select,os
sys.path.append('./Codes')
import tensorflow as tf
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pickle
import scipy.io.wavfile
import time
import pyaudio 

pathModel = './experiments/2017-10-29-10-16/temp/' #(200,100)


if not os.path.isdir(pathModel):
    print("could nt find path model {}".format(pathModel))
num_step = 100
bufferAudioSize = 800
fs = 22050

with tf.Session() as sess:
    saver = tf.train.import_meta_graph(pathModel+'myFinalModel.ckpt.meta')
    saver.restore(sess,tf.train.latest_checkpoint(pathModel))
    lastBuff = np.zeros((num_step-1,))
    graph = tf.get_default_graph()
    data = graph.get_tensor_by_name("placeHolder/data:0")
    prediction = graph.get_tensor_by_name("prediction:0")
    
    dataNonShaped = tf.placeholder(tf.float32, [bufferAudioSize,],name="inputFromADC")
    prevBuff = tf.placeholder(tf.float32, [num_step-1,],name = "EndofPreviousInputBufferNonShaped")
    newBuff = tf.concat([prevBuff,dataNonShaped],0) #size num_step-1+bufferAudioSize
    
    nextBuff = newBuff[-(num_step-1):] # save for next iteration
    
    my_indices = tf.constant(np.arange(bufferAudioSize))
    
    indices = (np.arange(num_step) +my_indices[:,tf.newaxis])
    dataShaped = tf.gather(newBuff,indices) # slice input vector into tenor of shape(audiobufferSize,num_step)

    def callback(in_data, frame_count, time_info, flag):
        if flag:
            print("Playback Error: {}".format(flag))
        global lastBuff

        audio_data = np.fromstring(in_data, dtype=np.float32)
        dataShapedToProcess,lastBuff = sess.run([dataShaped,nextBuff], feed_dict={dataNonShaped : audio_data, prevBuff : lastBuff})
        out = sess.run(prediction, feed_dict={data: dataShapedToProcess})
        return out, pyaudio.paContinue
    
    pa = pyaudio.PyAudio()
    
    stream = pa.open(format = pyaudio.paFloat32,
                     channels = 1,
                     rate = fs,
                     output = True,
                     input = True,
                     frames_per_buffer = bufferAudioSize,
                     stream_callback = callback)
    print("input latency {} s".format(stream.get_input_latency()))
    print("output latency {} s".format(stream.get_output_latency()))

    #stream.start_stream()
    while stream.is_active():   
        time.sleep(0.1)

    print("stream interrupted")   
    stream.stop_stream()
    stream.close()
    pa.terminate()