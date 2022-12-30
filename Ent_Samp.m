
function SE = Ent_Samp(name,m,R)
dataLoc = 'Results/Datas/s1.csv';
name = convertCharsToStrings(name);
DATA = readtable(dataLoc, 'PreserveVariableNames', true);
data = table2array(DATA);

% SE = Ent_Samp20200723(data,m,R) Returns the sample entropy value.
% inputs - data, single column time seres
%        - m, length of vectors to be compared
%        - R, radius for accepting matches (as a proportion of the
%          standard deviation)
%
% output - SE, sample entropy
% Remarks
% - This code finds the sample entropy of a data series using the method
%   described by - Richman, J.S., Moorman, J.R., 2000. "Physiological
%   time-series analysis using approximate entropy and sample entropy."
%   Am. J. Physiol. Heart Circ. Physiol. 278, H2039–H2049.
% May 2016 - Modified by John McCamley, unonbcf@unomaha.edu
%          - This is a faster version of the previous code.
% May 2019 - Modified by Will Denton
%          - Added code to check version number in relation to a server
%            and to automatically update the code.
% Jul 2020 - Modified by Ben Senderling, bmchnonan@unomaha.edu
%          - Removed the code that automatically checks for updates and
%            keeps a version history.
% Define r as R times the standard deviation
% Copyright 2020 Nonlinear Analysis Core, Center for Human Movement
% Variability, University of Nebraska at Omaha
%
% Redistribution and use in source and binary forms, with or without 
% modification, are permitted provided that the following conditions are 
% met:
%
% 1. Redistributions of source code must retain the above copyright notice,
%    this list of conditions and the following disclaimer.
%
% 2. Redistributions in binary form must reproduce the above copyright 
%    notice, this list of conditions and the following disclaimer in the 
%    documentation and/or other materials provided with the distribution.
%
% 3. Neither the name of the copyright holder nor the names of its 
%    contributors may be used to endorse or promote products derived from 
%    this software without specific prior written permission.
%
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS 
% IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
% THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
% PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
% CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
% EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
% PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
% PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
% LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
% NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
% SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
r = R * std(data);
N = length(data);

dij=zeros(N-m,m+1);
Bm=zeros(N-m,1);
Am=zeros(N-m,1);

for i = 1:N-m
    for k = 1:m+1
        dij(:,k) = abs(data(k:N-m+k-1)-data(i+k-1));
    end
    dj = max(dij(:,1:m),[],2);
    dj1 = max(dij,[],2);
    d = find(dj<=r);
    d1 = find(dj1<=r);
    nm = length(d)-1; % subtract the self match
    Bm(i) = nm/(N-m);
    nm1 = length(d1)-1; % subtract the self match
    Am(i) = nm1/(N-m);
end
Bmr = sum(Bm)/(N-m);
Amr = sum(Am)/(N-m);

SE = -log(double(Amr)/double(Bmr));