% clean=audioread('TFGClean.wav');
% dist=audioread('TFGDist.wav');
% 
% cleanMono=clean(:,1);
% DistMono=dist(:,1);
% 
% l=length(cleanMono);
% 
% %Train 60   Val 40
% limit=floor(l*0.6);
% 
% train=[cleanMono(1:limit), DistMono(1:limit)];
% val=[cleanMono(limit:end), DistMono(limit:end)];
% 
% save('train','train');
% 
% save('val','val');
filenameLin='Linea_Champion100Fender.wav';
filenameAmp='Ampli_Champion100Fender.wav';

clean=audioread(filenameLin);
dist=audioread(filenameAmp);

cleanMono=clean(:,1);
DistMono=dist(:,1);

l=length(cleanMono);

%Train 60   Val 40
limit=floor(l*0.6);
fin=8000000;
ini=3000000;

train=[cleanMono(ini:limit), DistMono(ini:limit)];
val=[cleanMono(limit:fin), DistMono(limit:fin)];

save(['train' filenameLin(1:end-3) 'mat'],'train');

save(['val' filenameLin(1:end-3) 'mat'],'val');

