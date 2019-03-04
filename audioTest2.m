Fs = 8000 % Frequency
Sb = 8    % Sample precision bits
Nc = 1    % Number of channels (1 - mono, 2- stereo)
t  = 5    % Recording time in seconds




% Plot the waveform.
% Read back from the file
[yy,fs] = audioread('OSR_us_000_0010_8k.wav');
plotWave_YW(1,yy,fs,'freq',1,'Novel')

soundsc(yy,fs); % Let's hear it