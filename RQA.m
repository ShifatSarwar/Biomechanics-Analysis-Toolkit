function [RP, RESULTS]=RQA(tau,dim,name, NORM, TYPE, ZSCORE, SETPARA, SETVALUE, plotOption)
%function [RP, RESULTS]=RQA(tau, dim, name)
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






