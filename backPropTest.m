% backPropTest.m
% created by Jenner Felton
% this script trains a three-layered network of units
% with the squashing activation function to associate 
% patterns using backpropagation

% Type of function can be defined as 'linear','logistic sigmoid', or 'tanh'
typeOfFunction = 'logistic sigmoid';

% Define as either: 'discrete' or 'continuous'
discrete = 'discrete';

InPat = input;
DesOut = desired;

a=0.1; % set the learning rate
tol=0.1; % set the tolerance
b=1; % set the bias
nIts=200000; % set the maximum number of allowed iterations
[nPat,nIn]=size(InPat); % find number of patterns and number of inputs 
[nPat,nOut]=size(DesOut); % find number of patterns and number of outputs 
pIndx=ceil(rand*nPat); % choose pattern pair at random
d=DesOut(pIndx,:); % set desired output to chosen output
x=[InPat(pIndx,:) b]'; % append the bias to the input vector
    
if 1 == strcmp(typeOfFunction,'logistic sigmoid')
     y=1./(1+exp(-V*x)); % compute the hidden unit response
     y=[y' b]'; % append the bias to the hidden unit vector
     z=1./(1+exp(-U*y)); % compute the output unit response      
 end
    
 if 1 == strcmp(typeOfFunction,'tanh')
     y = tanh(V*x);
     y = [y' b]';
     z = tanh(U*y);
 end
    
 if 1 == strcmp(typeOfFunction,'linear')
    y = V*x;
    y = [y' b]';
    z = U*y;
 end
  
 z(z>=.5) = 1;
 z(z<.5) = 0;
 
 z

errors = nnz(e); % compute number of errors
text1 = sprintf('Using the function %s with a %s output using %d hidden neurons.', typeOfFunction, discrete, nHid);
text3 = sprintf('Final classification errors %d out of %d output.', errors, nPat);
disp(text1) % display all the output text
if 1 == strcmp(discrete,'discrete')
    disp(text3)
end

    
    
    
    