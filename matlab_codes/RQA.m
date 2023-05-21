function [RP, RESULTS]=RQA(tau,dim,name, NORM, TYPE, ZSCORE, SETPARA, SETVALUE, plotOption)
%function [RP, RESULTS]=RQA(tau, dim, name)
% [RP, RESULTS]=RQA20200723(DATA,TYPE,EMB,DEL,ZSCORE,NORM,SETPARA,SETVALUE,plotOption)
% Inputs  - DATA, a double-variable with each dimension of the
%                 to-be-analyzed signal as a row of numbers in a separate
%                 column. If too many columns are present for the TYPE of
%                 analysis selected, the other columns will be ignored
%                 (i.e. for 'cRQA' only the first two columns will be
%                 used).
%         - TYPE, a string indicating which type of RQA to run (i.e.
%                 'RQA', 'cRQA', 'jRQA', 'mdRQA'). The default value is
%                 TYPE = 'RQA'.
%         - EMB, the number of embedding dimensions (i.e., EMB = 1 would
%                be no embedding via time-delayed surrogates, just using
%                the provided number of colums as dimensions. The default
%                value is EMB = 1.
%         - DEL, the delay parameter used for time-delayed embedding (if
%                EMB > 1). The default value is DEL = 1.
%         - ZSCORE, indicates, whether the data (i.e., the different
%                columns of DATA, being the different signals or
%                dimensions of a signal) should be z-scored before
%                performing MdRQA:
%                0 - no z-scoring of DATA
%                1 - z-score columns of DATA
%                The default value is ZSCORE = 0.
%         - NORM, the type of norm by with the phase-space is normalized.
%                The following norms are available:
%                'euc' - Euclidean distance norm
%                'max' - Maximum distance norm
%                'min' - Minimum distance norm
%                'non' - no normalization of phase-space
%                The default value is NORM = 'non'.
%         - SETPARA, the parameter which you would like to set a target
%                value for the recurrence plot (i.e. 'radius' or
%                'recurrence'). The default value is SETPARA = 'radius'.
%         - SETVALUE, sets the value of the selected parameter. If
%                SETVALUE = 1, then the radius will be set to 1 if SETPARA
%                = 'radius' or the radius will be adjusted until the
%                recurrence is equal to 1 if SETPARA = 'recurrence'. The
%                default value if SETPARA = 'radius' is 1. The default
%                value if SETPARA = 'recurrence' is 2.5.
%         - plotOption, is a boolean where if true the recurrence plot will
%                be created and displayed.
% Outputs - RP is a matrix holding the resulting recurrence plot.
%         - RESULTS is a structure holding the following recurrence
%           variables:
%           1.  DIM    - dimension of the input data (used for mdRQA)
%           2.  EMB    - embedding dimension used in the calculation of the
%                        distance matrix
%           3.  DEL    - time lag used in the calculation of the distance
%                        matrix
%           4.  RADIUS - radius used for the recurrence plot
%           5.  NORM   - type of normilization used for the distance matrix
%           6.  ZSCORE - whether or not zscore was used
%           7.  Size   - size of the recurrence plot
%           8.  %REC   - percentage of recurrent points
%           9.  %DET   - percentage of diagonally adjacent recurrent points
%           10. MeanL  - average length of adjacent recurrent points
%           11. MaxL   - maximum length of diagonally adjacent recurrent
%                        points
%           12. EntrL  - Shannon entropy of distribution of diagonal lines
%           13. %LAM   - percentage of vertically adjacent recurrent points
%           14. MeanV  - average length of diagonally adjacent recurrent
%                        points
%           15. MaxV   - maximum length of vertically adjacent recurrent
%                        points
%           16. EntrV  - Shannon entropy of distribution of vertical lines
%           17. EntrW  - Weighted entropy of distribution of vertical
%                        weighted sums
% Remarks
% - Computes a recurrence plot for either recurrence quantification
%   analysis (RQA), cross recurrence quantification analysis (cRQA), jount
%   recurrence quantification analysis (jRQA), or multidimensional
%   recurrence quantification analysis (mdRQA). Either radius or target
%   recurrence can be set.
% - When using CRQA, for the DEL parameter use the longer delay of the used
%   time series. For the EMB parameter use the larger embedding dimension
%   of the used time series.
% Reference:
% - Wallot, S., Roepstorff, A., & Monster, D. (2016). Multidimensional
%   Recurrence Quantification Analysis (MdRQA) for the analysis of
%   multidimensional time-series: A software implementation in MATLAB and
%   its application to group-level data in joint action. Frontiers in
%   Psychology, 7, 1835. http://dx.doi.org/10.3389/fpsyg.2016.01835
% - Eroglu, D., Peron, T. K. D., Marwan, N., Rodrigues, F. A., Costa, L. D.
%   F., Sebek, M., ... & Kurths, J. (2014). Entropy of weighted recurrence
%   plots. Physical Review E, 90(4), 042919.
%
% Jul 2016 Modified by Sebastian Wallot
%          - VERSION 1.0.0
%            28. July 2016 by Sebastian Wallot, Max Planck Insitute for
%            Empirical Aesthetics, Frankfurt, Germany & Dan M?nster, Aarhus
%            University, Aarhus, Denmark
% Jul 2017 Modified by Will Denton
%          - VERSION 1.1.0
%            06. July 2017 by Will Denton (wdenton@unomaha.edu), Troy Rand
%            (troyrand@gmail.com), and Casey Wiens (cwiens32@gmail.com),
%            Biomechanics Research Building, University of Nebraska at
%            Omaha. Changes include cleaning up some errors, making the
%            default input arguments function correctly, incorperating
%            other types of RQA (e.g. RQA, CRQA, JRQA), allowing %REC to be
%            set instead of radius, incorporating weighted recurrence
%            plots, and adding weighted entropy.
% May 2019 Modified by Will Denton
%          - VERSION 1.1.1 (05/09/2019)
%          - Added updates/patching.
%          - Added usage tracking to allow the Department of Biomechanics
%            at the University of Omaha see which codes and versions are
%            being used.
%          - Added error reporting to allow the Department of Biomechanics
%            at the University of Omaha to make improvements to this code.
% Nov 2019 Modified by Will Denton
%          - VERSION 1.1.2 (11/18/2019)
%          - Fixed usage and error reporting to work with MacOS.
%          - Fixed left plot to align with the recurrence plot when zoomed
%            in and panning around.
% Jul 2020 Modified by Ben Senderling, bmchnonan@unomaha.edu
%          - Removed automatic update code and version history code.
% Jul 2020 Modified by Ben Senderling, bmchnonan@unomaha.edu
%          - Reordered inputs. Made normalization strings capatals.
% May 2023 Updated for addition in Nonlinear Analysis Toolkit by
%          Shifat Sarwar, ssarwar@unomaha.edu
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


dataLoc = 'Results/Datas/s1.csv';
name = convertCharsToStrings(name);
SETVALUE = double(SETVALUE);

plotOption = 1;
DATA = readtable(dataLoc, 'PreserveVariableNames', true);
if plotOption == 1
    plotOption = true;
else 
    plotOption = false;
end
DATA = table2array(DATA);

%% Begin Code

dbstop if error

%% Set default parameters if no input exists
% If SETPARA is not specified, set to 'radius'
if isempty(SETPARA)
    SETPARA = 'radius';
end

% If SETVALUE is not specified, set to 1 if radius is set or 2.5 if perRec is set
if isempty(SETVALUE)
    switch lower(SETPARA)
        case {'radius','rad', 1}
            radius = 1;
            runSetRad = 0;
        case {'perrec','recurrence', 2}
            radiusStart = 0.01;
            radiusEnd = 0.5;
            runSetRad = 1;
            SETVALUE = 2.5;
    end
else
    switch lower(SETPARA)
        case {'radius','rad', 1}
            radius = SETVALUE;
            runSetRad = 0;
        case {'perrec','recurrence', 2}
            radiusStart = 0.01;
            radiusEnd = 0.5;
            runSetRad = 1;
    end
end

% If NORM is not specified, set to 'non'
if isempty(NORM)
    NORM = 'NON';
end

% If ZSCORE is not specified, set to 0
if isempty(ZSCORE)
    ZSCORE = 0;
end

% If DEL is not specified, set to 1
if isempty(tau)
    tau = 1;
end

% If EMB is not specified, set to 1
if isempty(dim)
    dim = 1;
end

% If EMB is not specified, set to 1
if isempty(TYPE)
    TYPE = 'RQA';
end

% If z score is selected then z score the data
if ZSCORE
    DATA = zscore(DATA);
end

%% Begin code
% Set DIM and select proper column(s) of data if too many exist

c = size(DATA,2);
switch upper(TYPE)
    case 'RQA'
        DIM = 1;
        if c > 1
            DATA = DATA(:,1);
            warning('More than one column of data. Only using first column.');
        end
    case {'CRQA','CROSS'}
        DIM = 2;
        if c > 2
            DATA = DATA(:,1:2);
            warning('More than two columns of data. Only using first two columns.');
        end
    case {'JRQA','JOINT'}
        DIM = c;
        if c < 2
            error('Input data must have at least two columns.');
        end
    case {'MDRQA','MD','MULTI'}
        DIM = c;
end

% Embed the data
if dim > 1
    for i = 1:dim
        tempDATA(1:length(DATA)-(dim-1)*tau,1+DIM*(i-1):DIM*i) = DATA(1+(i-1)*tau:length(DATA)-(dim-i)*tau,:);
    end
    DATA = tempDATA;
    clear tempDATA
end

% Calculate distance matrix based on the type of RQA
switch upper(TYPE)
    case 'RQA'
        a{1}=pdist2(DATA,DATA);
        a{1}=abs(a{1})*-1;
    case {'CRQA','CROSS'}
        a{1}=pdist2(DATA(:,1:DIM:end),DATA(:,2:DIM:end));
        a{1}=abs(a{1})*-1;
    case {'JRQA','JOINT'}
        for i = 1:c
            a{i}=pdist2(DATA(:,i:DIM:end),DATA(:,i:DIM:end));
            a{i}=abs(a{i})*-1;
        end
    case {'MDRQA','MD','MULTI'}
        a{1}=pdist2(DATA,DATA);
        a{1}=abs(a{1})*-1;
end


% Normalize distance matrix
if contains(NORM, 'EUC')
    for i = 1:length(a)
        b = mean(a{i}(a{i}<0));
        b = -sqrt(abs(((b^2)+2*(DIM*dim))));
        a{i} = a{i}/abs(b);
    end
elseif contains(NORM, 'MIN')
    for i = 1:length(a)
        b = max(a{i}(a{i}<0));
        a{i} = a{i}/abs(b);
    end
elseif contains(NORM, 'MAX')
    for i = 1:length(a)
        b = min(a{i}(a{i}<0));
        a{i} = a{i}/abs(b);
    end
elseif contains(NORM, 'NON')
    %do nothing
else
    error('No appropriate norm parameter specified.');
end

wrp = a;
for i = 1:size(a,2)-1
    wrp{i+1} = wrp{i}.*wrp{i+1};
end
if i
    wrp = -(abs(wrp{i+1})).^(1/(i+1));
end
if iscell(wrp)
    wrp = wrp{1};
end

% Calculate recurrence plot
switch lower(SETPARA)
    case {'radius','rad', 1}
        [perRec, diag_hist, vertical_hist,A] = recurrenceMethod(a,radius);
    case {'perrec','recurrence', 2}
        [perRec, diag_hist, vertical_hist, radius, A] = setRadius(radiusStart);
end

%% Calculate RQA variabes
RESULTS.DIM = DIM;
RESULTS.EMB = dim;
RESULTS.DEL = tau;
RESULTS.RADIUS = radius;
RESULTS.NORM = NORM;
RESULTS.ZSCORE = ZSCORE;
RESULTS.Size=length(A);
RESULTS.REC = perRec;
if RESULTS.REC > 0
    RESULTS.DET=100*sum(diag_hist(diag_hist>1))/sum(diag_hist);
    RESULTS.MeanL=mean(diag_hist(diag_hist>1));
    RESULTS.MaxL=max(diag_hist);
    [count,bin]=hist(diag_hist(diag_hist>1),min(diag_hist(diag_hist>1)):max(diag_hist));
    total=sum(count);
    p=count./total;
    del=find(count==0); p(del)=[];
    RESULTS.EntrL=-sum(p.*log2(p));
    RESULTS.LAM=100*sum(vertical_hist(vertical_hist>1))/sum(vertical_hist);
    RESULTS.MeanV=mean(vertical_hist(vertical_hist>1));
    RESULTS.MaxV=max(vertical_hist);
    [count,bin]=hist(vertical_hist(vertical_hist>1),min(vertical_hist(vertical_hist>1)):max(vertical_hist));
    total=sum(count);
    p=count./total;
    del=find(count==0); p(del)=[];
    RESULTS.EntrV=-sum(p.*log2(p));
    RESULTS.EntrW=RQA_WeightedEntropy( wrp );
else
    RESULTS.DET=NaN;
    RESULTS.MeanL=NaN;
    RESULTS.MaxL=NaN;
    RESULTS.EntrL=NaN;
    RESULTS.LAM=NaN;
    RESULTS.MeanV=NaN;
    RESULTS.MaxV=NaN;
    RESULTS.EntrV=NaN;
    RESULTS.EntrW=NaN;
end
RP=imrotate(1-A,90);

%% PLOT
if plotOption
    scrsz = get(0,'ScreenSize');
    f = figure('Position',[scrsz(3)/4 scrsz(4)/4 scrsz(3)/3 scrsz(4)/2]);tabgp = uitabgroup(f);
    binary = uitab(tabgp,'Title','Binary');
    heatmap = uitab(tabgp,'Title','Heatmap');
    % Binary Plot (Tab 1)
    a1 = axes('Parent',binary,'Position', [0 0 1 1], 'Visible', 'off');
    ax(1) = axes('Parent',binary,'Position',[.375 .35 .58 .6], 'FontSize', 8);
    imagesc(ax(1),RP); colormap(gray);
    title(['DIM = ', num2str(DIM), '; EMB = ',num2str(dim), '; DEL = ', num2str(tau), '; RAD = ', num2str(radius), '; NORM = ',num2str(NORM), '; ZSCORE = ',num2str(ZSCORE)],'FontSize',8)
    xlabel('X(i)','Interpreter','none', 'FontSize', 10);
    ylabel('Y(j)','Interpreter','none', 'FontSize', 10);
    set(gca,'XTick',[ ]);
    set(gca,'YTick',[ ]);
    switch upper(TYPE)
        case {'RQA','MDRQA','MD','MULTI'}
            ax(2) = axes('Parent',binary,'Position',[.375 .1 .58 .15], 'FontSize', 8);
            plot(1:length(DATA(:,1)), DATA(:,1), 'k-');
            xlim([1 length(DATA(:,1))]);
            ax(3) = axes('Parent',binary,'Position',[.09 .35 .15 .6], 'FontSize', 8);
            plot(flip(DATA(:,1)), 1:length(DATA(:,1)), 'k-');
            ylim([1 length(DATA(:,1))]);
            set (ax(3),'Ydir','reverse');
        case {'CRQA','CROSS'}
            ax(2) = axes('Parent',binary,'Position',[.375 .1 .58 .15], 'FontSize', 8);
            plot(1:length(DATA(:,1)), DATA(:,1), 'k-');
            xlim([1 length(DATA(:,1))]);
            ax(3) = axes('Parent',binary,'Position',[.09 .35 .15 .6], 'FontSize', 8);
            plot(flip(DATA(:,2)), 1:length(DATA(:,2)), 'k-');
            ylim([1 length(DATA(:,1))]);
            set (ax(3),'Ydir','reverse');
        case {'JRQA','JOINT'}
            for i = 1:c
                ax(2) = axes('Parent',binary,'Position',[.375 .1 .58 .15], 'FontSize', 8);
                plot(1:length(DATA(:,1)), DATA(:,i),'k-');
                xlim([1 length(DATA(:,1))]);
                ax(3) = axes('Parent',binary,'Position',[.09 .35 .15 .6], 'FontSize', 8);
                plot(flip(DATA(:,1)), 1:length(DATA(:,i)),'k-');
                ylim([1 length(DATA(:,1))]);
                set (ax(3),'Ydir','reverse');
            end
    end
    set(gcf, 'CurrentAxes', a1);
    str(1) = {['%REC = ', sprintf('%.2f',RESULTS.REC)]};
    text(.1, 0.27, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['%DET = ', sprintf('%.2f',RESULTS.DET)]};
    text(.1, .24, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['MaxL = ', sprintf('%.0f',RESULTS.MaxL)]};
    text(.1, .21, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['MeanL = ', sprintf('%.2f',RESULTS.MeanL)]};
    text(.1, .18, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['EntrL = ', sprintf('%.2f',RESULTS.EntrL)]};
    text(.1, .15, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['%LAM = ', sprintf('%.2f',RESULTS.LAM)]};
    text(.1, .12, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['MaxV = ', sprintf('%.0f',RESULTS.MaxV)]};
    text(.1, .09, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['MeanV = ', sprintf('%.2f',RESULTS.MeanV)]};
    text(.1, .06, str, 'FontSize', 8, 'Color', 'k');
    str(1) = {['EntrV = ', sprintf('%.2f',RESULTS.EntrV)]};
    text(.1, .03, str, 'FontSize', 8, 'Color', 'k');
    
    % Heatmap Plot (Tab 2)
    a2 = axes('Parent',heatmap,'Position', [0 0 1 1], 'Visible', 'off');
    ax(4) = axes('Parent',heatmap,'Position',[.375 .35 .58 .6], 'FontSize', 8);
    imagesc(ax(4),imrotate(-1*wrp,90));
    title(['DIM = ', num2str(DIM), '; EMB = ',num2str(dim), '; DEL = ', num2str(tau), '; RAD = ', num2str(radius), '; NORM = ',num2str(NORM), '; ZSCORE = ',num2str(ZSCORE)],'FontSize',8)
    xlabel('X(i)','Interpreter','none', 'FontSize', 10);
    ylabel('Y(j)','Interpreter','none', 'FontSize', 10);
    set(gca,'XTick',[ ]);
    set(gca,'YTick',[ ]);
    switch upper(TYPE)
        case {'RQA','MDRQA','MD','MULTI'}
            ax(5) = axes('Parent',heatmap,'Position',[.375 .1 .58 .15], 'FontSize', 8);
            plot(1:length(DATA(:,1)), DATA(:,1), 'k-');
            xlim([1 length(DATA(:,1))]);
            ax(6) = axes('Parent',heatmap,'Position',[.09 .35 .15 .6], 'FontSize', 8);
            plot(flip(DATA(:,1)), 1:length(DATA(:,1)), 'k-');
            ylim([1 length(DATA(:,1))]);
            set (ax(6),'Ydir','reverse');
        case {'CRQA','CROSS'}
            ax(5) = axes('Parent',heatmap,'Position',[.375 .1 .58 .15], 'FontSize', 8);
            plot(1:length(DATA(:,1)), DATA(:,1), 'k-');
            xlim([1 length(DATA(:,1))]);
            ax(6) = axes('Parent',heatmap,'Position',[.09 .35 .15 .6], 'FontSize', 8);
            plot(flip(DATA(:,2)), 1:length(DATA(:,2)), 'k-');
            ylim([1 length(DATA(:,1))]);
            set (ax(6),'Ydir','reverse');
        case {'JRQA','JOINT'}
            for i = 1:c
                ax(5) = axes('Parent',heatmap,'Position',[.375 .1 .58 .15], 'FontSize', 8);
                plot(1:length(DATA(:,1)), DATA(:,i),'k-');
                xlim([1 length(DATA(:,1))]);
                ax(6) = axes('Parent',heatmap,'Position',[.09 .35 .15 .6], 'FontSize', 8);
                plot(flip(DATA(:,1)), 1:length(DATA(:,i)),'k-');
                ylim([1 length(DATA(:,1))]);
                set (ax(6),'Ydir','reverse');
            end
    end
    set(gcf, 'CurrentAxes', a2);
    str(1) = {['EntrW = ', sprintf('%.2f',RESULTS.EntrW)]};
    text(.1, 0.27, str, 'FontSize', 8, 'Color', 'k');
    linkaxes(ax([1,4]),'xy');
    linkaxes(ax([1,2,4,5]),'x');
    linkaxes(ax([1,3,4,6]),'y');
    
end

%% Function for setting radius to achieve a certain recurrence
    function [perRec, diag_hist, vertical_hist, radiusFinal,A] = setRadius(radius)
        % Find the radius to provide target % recurrence
        [perRec, ~, ~, ~] = recurrenceMethod(a,radius);
        while perRec == 0 || perRec > SETVALUE % SETVALUE
            % if radius is too small
            display('Minimum radius has been adjusted...');
            %             radiusEnd = radius + 0.5;
            if perRec == 0
                radius = radius*2;
            elseif perRec > SETVALUE
                radius = radius / 1.5;
                %                 radiusEnd =  radius + 0.5;
            end
            [perRec, ~, ~, ~] = recurrenceMethod(a,radius);
        end
        
        [perRec, ~, ~, ~] = recurrenceMethod(a,radiusEnd);
        while perRec < SETVALUE
            % if radiusEnd is too large
            display('Maximum radius has been increased...');
            radiusEnd = radiusEnd*2;
            [perRec, ~, ~, ~] = recurrenceMethod(a,radiusEnd);
        end
        
        radius

        % Search for radius with target % recurrence
        wb = waitbar(0,['Finding radius to give %REC = ',num2str(SETVALUE), ' Please wait...']);    % create wait bar to display progress
        lv = radius;    % set low value
        hv = radiusEnd; % set high value
        target = SETVALUE;  % designate what percent recurrence is wanted
        iter = 15; % Number of iterations to find radius
        for  i1 = 1:iter
            mid(i1) = (lv(i1)+hv(i1))/2;   % find midpoint between hv and lv
            rad(i1) = mid(i1);    % new radius for this iteration
            i1
            %Compute recurrence matrix
            [perRec, diag_hist, vertical_hist,A] = recurrenceMethod(a, rad(i1));
            
            perRecIter(i1) = perRec;  % set percent recurrence
            perRec
            if perRecIter(i1) < target
                % if percent recurrence is below target percent recurrence
                hv(i1+1) = hv(i1);
                lv(i1+1) = mid(i1);
            else
                % if percent recurrence is above or equal to target percent recurrence
                lv(i1+1) = lv(i1);
                hv(i1+1) = mid(i1);
            end
            waitbar(i1/iter,wb); % update wait bar
        end
        
        close(wb)
        perRecFinal = perRecIter(end);  % set final percent recurrence
        radiusFinal = rad(end);      % set radius for final percent recurrence
        disp(['% recurrence = ',num2str(perRecFinal),', radius = ',num2str((radiusFinal))])
    end

    function [perRec, diag_hist, vertical_hist, A] = recurrenceMethod(A, radius)
        if ~iscell(A)
            A = {A};
            
        end
        for i2 = 1:length(A)
            A{i2} = A{i2}+radius;
            A{i2}(A{i2} >= 0) = 1;
            A{i2}(A{i2} < 0) = 0;
        end
        
        if length(A) > 1
            for i3 = 1:length(A)-1
                A{i3+1} = A{i3}.*A{i3+1};
            end
            A = A{i3+1};
        else
            A = A{1};
        end
        
        diag_hist = [];
        vertical_hist = [];
        for i4 = -(length(DATA)-1):length(DATA)-1 % caluculate diagonal line distribution
            C=diag(A,i4);
            % bwlabel is taking each diagonal line and looking for the 1's, it will
            % return increasing numbers for each new instance of 1's, for example
            % the input vector [0 1 1 0 1 0 1 1 0 0 1 1 1] will return
            %                  [0 1 1 0 2 0 3 3 0 0 4 4 4]
            d=bwlabel(C,8);
            % tabulate counts the instances of each integer, therefore the line
            % lengths
            d = nonzeros(hist(d)); % This speeds up the code 30-40% and is simpler to understand.
            if i4 ~= 0
                d=d(2:end);
            end
            % diag_hist is creating one long array of all of the line lengths for
            % all of the diagonals
            diag_hist(length(diag_hist)+1:length(diag_hist)+length(d))=d;
        end
        
        % This removes the line of identity in RQA, jRQA, and mdRQA
        if ~contains(upper(TYPE),{'CROSS','CRQA'})
            diag_hist=diag_hist(diag_hist<max(diag_hist));
            if isempty(diag_hist)
                diag_hist=0;
            end
        end
        
        for i5=1:length(DATA) % calculate vertical line distribution
            C=(A(:,i5));
            v=bwlabel(C,8);
            v=nonzeros(hist(v));
            if v(1,1)~=length(DATA)
                v=v(2:end);
            end
            vertical_hist(length(vertical_hist)+1:length(vertical_hist)+length(v))=v;
        end
        
        % Calculate percent recurrence
        if ~contains(upper(TYPE),{'CROSS','CRQA'})
            perRec = 100*(sum(sum(A))-length(A))/(length(A)^2-length(A));
        else
            perRec = 100*(sum(sum(A)))/(length(A)^2);
        end
    end
%% Calculate entropy of weighted recurrence plot
    function [ Swrp ] = RQA_WeightedEntropy( WRP )
        N = length(WRP);
        for j = 1:N
            si(j) = sum(WRP(:,j));
        end
        mi = min(si);
        ma = max(si);
        m = (ma - mi)/49;
        I = 1;
        S = sum(si);
        for s = mi:m:ma
            P = sum( si(si >= s & si < (s+m)) );
            p1( I ) = P / S;
            I = I+1;
        end
        for I = 1:length(p1)
            pp(I) = (p1(I)*log(p1(I)));
        end
        pp(isnan(pp)) = 0;
        Swrp = -1*(sum(pp));
    end

end






