Fs = 8000 % Frequency
Sb = 8    % Sample precision bits
Nc = 1    % Number of channels (1 - mono, 2- stereo)
t  = 5    % Recording time in seconds
%Read the audio file
[y,fs] = audioread('OSR_us_000_0010_8k.wav');
%play 8k wave file first
sound(y,fs);
plotWave_YW(1,y,fs,'freq',1,'Novel 8k')
pause(35)
%Change sampling rate
fs2= 2*fs;
audiowrite('OSR_us_000_0010_16k.wav',y,fs2);
%Read the data back into MATLAB using audioread
[y,fs2] = audioread('OSR_us_000_0010_16k.wav');
plotWave_YW(1,y,fs2,'freq',1,'Novel 16k')
sound(y, fs2);
 

