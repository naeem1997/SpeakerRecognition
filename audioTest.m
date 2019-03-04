Fs = 8000 % Frequency
Sb = 8    % Sample precision bits
Nc = 1    % Number of channels (1 - mono, 2- stereo)
t  = 5    % Recording time in seconds
x = cos(2*pi*2000*t)+1/2*sin(2*pi*4000*(t-pi/4))+1/4*cos(2*pi*8000*t);
[P,Q] = rat(16e3/Fs);
abs(P/Q*Fs-16000)
xnew = resample(x,P,Q);

recObj = audiorecorder(Fs,Sb,Nc);
get(recObj);
disp('Start speaking.')
recordblocking(recObj, t);
disp('End of Recording.');

% Play back the recording.
% play(recObj);

% Store data in double-precision array.
myRecording = getaudiodata(recObj);
audiowrite('howAreYou.wav', myRecording,Fs);

% Plot the waveform.
plot(myRecording);
% Read back from the file
%[yy,fs] = audioread('howAreYou.wav');
P8_1 = audioplayer(x,8000);
P16 = audioplayer(xnew,16000);
play(P8_1)
play(P16)

soundsc(yy,fs); % Let's hear it