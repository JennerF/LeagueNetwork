

% Defines input, desired, and title so that backProp can run

data = importdata('InputData2.xls');
[rows,cols] = size(data);
[trainInd, valInd, testInd] = dividerand(rows, 0.7, 0.0, 0.3);

input = data(:,1:24);
desired = data(:,end);

% input = data(trainInd,1:24);
% desired = data(trainInd,end);
%title = 'TrainingNetwork';

% backProp;
% input = data(testInd, 1:24);
% desired = data(testInd, end);
% title = 'TestingNetwork';
% backPropTest;
