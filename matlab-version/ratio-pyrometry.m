B = imread("/Users/michael/Projects/firelab-general/examples/01-0001-cropped.png");

nrows = height(B);
ncolumns = width(B);

rdc = 7.7; % This, and the next 2 terms, are dark current values.
gdc = 11.5; % They’re representative for a single camera orientation,
bdc = 4.4; % but they’re negligible in general.
GSdc = (rdc+gdc+bdc)/3;

iso = 64;
t = 0.5;
f = 2.4;

rawred = double(B(:,:,1));
rawgreen = double(B(:,:,2));
rawblue = double(B(:,:,3));
rawblue(rawblue > 65534) = 0;
rawGS = double(rgb2gray(B));

normred = ((rawred-rdc)*(f^2))/(iso*t);
normgreen = ((rawgreen-gdc)*(f^2))/(iso*t);
normblue = ((rawblue-bdc)*(f^2))/(iso*t);

GR = normgreen./normred; % Green-to-Red normalized pixel ratio
GR2 = log10(GR); % Log-base-10 of above ratio
GR2(imag(GR2) > 0) = 0; % Removes any imaginary entries
logGR = GR2; % Redefinition for calculations

%% Application of ratio pyrometry curve fit
RT = (362.73.*(logGR.^3) + 2186.7.*(logGR.^2) + 4466.5.*(logGR) + 3753.5); % New Camera Ratio Temp

%% Removal of 600-1200 range (Ratio)
RT(RT < 600 | RT > 1200) = 0; % BB Calibration Temperature range

%% 50% rule (Ratio)
RT2 = RT; % This section and below apply a noise reduction algorithm
% - if 50% of pixels around each pixel are 0, set that pixel to 0 as well
for i = 4:(nrows-4)
    for j = 4:(ncolumns-4)
        if nnz(RT(i-3:i+3,j-3:j+3)) < 25
            RT2(i,j) = 0;
        else
            RT2(i,j) = RT(i,j);
        end
    end 
end

%% MATLAB display
RT3=RT2; % Left in b/c some images need to be flipped for proper
% display - to do this, the command would instead be "RT3 = flip(RT2)
RatioAverageTemp = mean(nonzeros(RT3)); % Average surface temperature
Pixel = nnz(RT3); % Temp pixel count, to contextualize
