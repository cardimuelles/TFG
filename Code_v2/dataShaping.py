#!/usr/bin/python
# -*- coding: latin-1 -*-
"""datashaping loading in file at each batch, format [batchSize,numStep]"""
import scipy.io as sio
import numpy as np


# take input matrix and return shuffled train/test input/input
def splitData(matrix,num_step,trainTestRatio,maxSize,features):
    matrixIn = matrix[:maxSize,0]
    matrixOut = matrix[:maxSize,1]
    trainSize = int(len(matrixIn)*trainTestRatio)
    testSize = maxSize-trainSize
    reshapedInput  = []
    reshapedOutput = []
    nbExample = len(matrixIn)-num_step
    for i in range(nbExample):
        temp_list = matrixIn[i:i+num_step]
        temp_list_out = [matrixOut[i+num_step-1]]
        reshapedInput.append(np.array(temp_list))
        reshapedOutput.append(np.array(temp_list_out))
    inputS = np.float32(np.array((reshapedInput)).reshape(maxSize-num_step,num_step,features))
    outputS = np.float32(np.array((reshapedOutput)).reshape(maxSize-num_step,1,features))
    trainInput = inputS[:trainSize]
    trainOutput = outputS[:trainSize]
    testInput = inputS[trainSize:]
    testOutput = outputS[trainSize:]
    return trainInput,trainOutput,testInput,testOutput

def shapeData(matrix,num_step,maxSize,features):
    if maxSize==-1:
        maxSize=len(matrix)
    matrixIn = matrix[:maxSize,0]
    matrixOut = matrix[:maxSize,1]
    reshapedInput  = []
    reshapedOutput =[]
    nbExample = len(matrixIn)-num_step
    for i in range(nbExample):
        temp_list = matrixIn[i:i+num_step]
        temp_list_out = [matrixOut[i+num_step-1]]
        reshapedInput.append(np.array(temp_list))
        reshapedOutput.append(np.array(temp_list_out))
    reshapedInput = np.float32(np.array(reshapedInput).reshape(maxSize-num_step,num_step,features))
    reshapedOutput = np.float32(np.array(reshapedOutput).reshape(maxSize-num_step,1,features))
    return reshapedInput, reshapedOutput 

def shuffleMatrix(data):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    return [data[i] for i in shuffled_indices]


def shapeDataRealTime(frame,num_step,features):
    maxSize=len(frame)
    reshapedInput  = []
    reshapedOutput =[]
    nbExample = len(frame)-num_step
    for i in range(nbExample):
        temp_list = frame[i:i+num_step]
        reshapedInput.append(np.array(temp_list))
    reshapedInput = np.float32(np.array(reshapedInput).reshape(maxSize-num_step,num_step,features))
    return reshapedInput



