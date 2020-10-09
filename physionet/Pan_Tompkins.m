clc;

close all;

filename = 'samples.csv';
delimiter = ',';
startRow = 3;

%% Format for each line of text:
%   column1: text (%s)
%	column2: double (%f)
%   column3: double (%f)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%s%f%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Allocate imported array to column variable names
Elapsedtime = dataArray{:, 1};
MLII = dataArray{:, 2};
V5 = dataArray{:, 3};


%% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans;

%% Begin PT Algorithm
fs=250;
[lp_coeff,~]=fir1(6,15/fs/2,'low');
[hp_coeff,~]=fir1(6,5/fs/2,'high');

signal = V5;

low_pass = filter(lp_coeff, 1, signal);
band_pass = filter(hp_coeff, 1, low_pass);

diffed = diff(band_pass);

squared = diffed.^2;

averaged = conv(squared,ones(1,36));

plot(signal,'DisplayName','Signal','LineWidth',1); hold on; plot(band_pass,'DisplayName','Filtered','LineWidth',1);
legend;

figure(); 

plot(diffed, 'DisplayName','Diffed','LineWidth',1); 
hold on; 
plot(squared,'DisplayName','Squared','LineWidth',1); 
plot(averaged,'DisplayName','Averaged','LineWidth',1);
legend;