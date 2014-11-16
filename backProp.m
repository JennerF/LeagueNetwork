% backProp.m
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
nHid=30; % set the number of hidden units
[nPat,nIn]=size(InPat); % find number of patterns and number of inputs 
[nPat,nOut]=size(DesOut); % find number of patterns and number of outputs 
V=rand(nHid,nIn+1)*2-1; % set initial input-hidden connectivity matrix
U=rand(nOut,nHid+1)*2-1; % set initial hidden-output connectivity matrix
deltaV=zeros(nHid,nIn+1); % define input-hidden change matrices
deltaU=zeros(nOut,nHid+1); % define hidden-output change matrices
maxErr=10; % set the maximum error to an initially high value
MSE = 10;
MSEARRAY = zeros(1,nIts);

for c=1:nIts, % for each learning iteration
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
    
    e=d-z'; % find the error vector
    x=x';y=y';z=z'; % convert column to row vectors
        
    if 1 == strcmp(typeOfFunction,'logistic sigmoid')
        zg=e.*(z.*(1-z)); % compute the output error signal
        yg=(y.*(1-y)).*(zg*U); % compute hidden error signal
            
        Inb=[InPat b*ones(nPat,1)]; % append bias to all input patterns
        Hid=(1./(1+exp(-V*Inb')))'; % find hid response to all patterns
        Hidb=[Hid b*ones(nPat,1)]; % append bias to all hidden vectors
        Out=(1./(1+exp(-U*Hidb')))'; % find out response to all patterns
    end
        
    if 1 == strcmp(typeOfFunction,'tanh')
        zg = e.* (1-z.^2);
        yg = (1-y.^2).*(zg*U);

        Inb=[InPat b*ones(nPat,1)]; % append bias to all input patterns
        Hid=(tanh(V*Inb'))'; % find hid response to all patterns
        Hidb=[Hid b*ones(nPat,1)]; % append bias to all hidden vectors
        Out=(tanh(U*Hidb'))'; % find out response to all patterns
    end

    if 1 == strcmp(typeOfFunction,'linear')
        zg = e.*z;
        yg = y.*(zg*U);

        Inb=[InPat b*ones(nPat,1)]; % append bias to all input patterns
        Hid=(V*Inb')'; % find hid response to all patterns
        Hidb=[Hid b*ones(nPat,1)]; % append bias to all hidden vectors
        Out=(U*Hidb')'; % find out response to all patterns
    end

    deltaU=a*zg'*y; % compute the change in hidden-output weights
    deltaV=a*yg(1:nHid)'*x; % compute change in input-hidden weights
    U=U+deltaU; % update the hidden-output weights
    V=V+deltaV; % update the input-hidden weights

    if 1 == strcmp(discrete,'discrete')
        if 1 == strcmp(typeOfFunction, 'logistic sigmoid')
            Out(Out>=.5) = 1;
            Out(Out<.5) = 0;
        else
            Out(Out>0) = 1;
            Out(Out<=0) = 0;
        end
    end

    MSE = (sum((DesOut-Out).^2))/nPat; % find the Mean Squared Error
    MSEARRAY(1,c) = MSE; % make an array for plotting later
        
    if MSE<tol, break, end, % break if all errors within tolerance
end % end training loop

errors = nnz(DesOut - Out); % compute number of errors
text1 = sprintf('Using the function %s with a %s output using %d hidden neurons.', typeOfFunction, discrete, nHid);
text2 = sprintf('%s took %d iterations. Final MSE was %d.', title, c, MSE);
text3 = sprintf('Final classification errors %d out of %d output.', errors, nPat);
disp(text1) % display all the output text
disp(text2)
if 1 == strcmp(discrete,'discrete')
    disp(text3)
end
disp(' ')

title1 = title; % allow us to use the function title, so we can edit the graph
clear title;

plot(MSEARRAY) % plot our data
xlabel('Epoch Number')
ylabel('MSE')
title(title1)


   