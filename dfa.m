function [a, r2, out_a, out_l] = dfa(name, n_min, n_max, n_length, plotOption)
ts = 'Results/Datas/s1.csv';
ts = readtable(ts, 'PreserveVariableNames', true);
ts = table2array(ts);
name = convertCharsToStrings(name);
dbstop if error

%% Input handling

if size(ts, 1) > size(ts, 2) % ts should be row vector
     ts = ts';
end
n_min = double(n_min);
n_max = double(n_max);
n_bp =linspace(log10(n_min), log10(n_max), n_length+1)'; % calculate breakpoints for fit line (spaced evenly in log space)

n = (10:length(ts)/9)'; % calculate F for every possible n (makes plot nice)

F = dfa_fluct(ts, n); % calculate F for every n

[F_fit, n_fit, a, r2, logF_fit] = dfa_fit_average(n, F, n_bp); % fit line over n_fit using averaging method

dfa_plot(n, F, n_fit, F_fit, logF_fit, name); % produce plot of log F vs log n
string = ['\alpha = ', num2str(a, '%.2f'), newline, 'r^2 = ', num2str(r2, '%.2f')];
x_lim = get(gca, 'XLim');
y_lim = get(gca, 'YLim');
text(x_lim(2)/2, y_lim(1)*2, string, 'HorizontalAlignment', 'right', 'VerticalAlignment', 'bottom')

out_a=[n,F];
out_l=[n_fit,F_fit,logF_fit];
end


function F = dfa_fluct(ts, n)

zero_th = .000001; % F < this value is equivalent to F = 0

F2=zeros(length(n),1);
F=zeros(length(n),1);
for nn = 1:length(n)
    num_boxes = floor(length(ts)/n(nn));
    B = ts(1:num_boxes*n(nn))';
    
    % "the ... time series (of total length N) is first
    % integrated, y(k) = sum(i=1:k)(B(i) - B_ave), where B(i) is the ith
    % [value of the time series] and B_ave is the average [value]"
    B_ave = nanmean(B);
    B_nonan = fillmissing(B,'linear','SamplePoints',1:length(B)); % deal with NaN values for integration step 
    y_nonan = cumsum(B_nonan - B_ave);
    y = y_nonan;
    y(isnan(B)) = NaN; % replace NaN values in integrated series
    
    y_n=zeros(num_boxes,1);
    % "the integrated time series is divided into boxes of equal length, n"
    for k = 0:num_boxes - 1
        
        % "in each box of length n, a least-squares line is fit to the data
        % (representing the trend in that box) ... denoted by y_n(k)"
        X = k*n(nn) + 1:(k + 1)*n(nn);
        Y = y_nonan(X); % fit using interpolated series
        m_b = polyfit(X, Y, 1);
        y_n(X) = polyval(m_b, X);
    end
    
    % "detrend the integrated time series, y(k), by subtracting the local
    % trend, y_n(k) .... The root-mean-square fluctuation ... is calculated
    % by [Equation 1]"
    F2(nn) = nanmean((y - y_n).^2); % ignores NaN values
    
    F(nn) = sqrt(F2(nn));
    
% "This computation is repeated over all time scales (box sizes)"
end

% "the fluctuations can be characterized by a scaling exponent a, the slope
% of the line relating log F(n) to log n"
F(F < zero_th) = NaN; % removes F = 0 from linear fit

end

function [F_fit, n_fit, a, r2, logF_fit] = dfa_fit_average(n, F, n_bp)
% [F_fit, n_fit, a, r2, Xave, Yave, logF_fit] = dfa_fit_average(n, F, n_bp)
% Inputs  - n, vector of box sizes
%         - F, vector of fluctuations
%         - n_bp, vector of bin break points
% Outputs - F_fit, vector of best fit values
%         - n_fit, vector of bin centers
%         - a, slope of best fit line
%         - r2, r^2 of best fit line
% Remarks
% - DFA_FIT Returns best fit line, slope and r^2 of log-log of fluctuations
%   vs. box size over given range of box sizes, using average log(F) over a
%   range of log(n_i) to log(n_i+1).
% References:
% - Peng, C. K., Havlin, S., Stanley, H. E., & Goldberger, A. L. (1995).
%   Quantification of scaling exponents and crossover phenomena in 
%   nonstationary heartbeat time series. Chaos: An Interdisciplinary 
%   Journal of Nonlinear Science, 5(1), 82-87.
% Prior    - Created by Naomi Kochi
% Jul 2020 - Modified by Ben Senderling
%          - Reformated comments. Added array pre-allocation.
%% Begin code
% "the fluctuations can be characterized by a scaling exponent a, the slope
% of the line relating log F(n) to log n"

F10=log10(F)';
n10=log10(n)';

Xave=zeros(length(n_bp)-1,1);
Yave=zeros(length(n_bp)-1,1);
for i = 1:length(n_bp) -1
    Xave(i) = mean((n_bp(i:i+1)))'; % calculate center of bin
    Yave(i) = mean((F10(n10 >= n_bp(i) & n10 < n_bp(i+1))))'; % average all values in bin
end
[P, S] = polyfit(Xave, Yave, 1); % can't fit log(0) or log(NaN)
logF_fit = polyval(P, Xave);

F_fit = 10.^Yave; % return best fit 'line' in linear space
n_fit = 10.^Xave;
logF_fit=10.^logF_fit;

a = P(1); % return DFA scaling exponent (slope of best fit line)
r2 = 1 - S.normr^2 / norm(Yave(isfinite(Yave)) - mean(Yave(isfinite(Yave))))^2; % return r^2 of best fit line

end
function hAxObj = dfa_plot(n, F, n_fit, F_fit, logF_fit, name)

loglog(n, F, 'b.', n_fit, F_fit, 'ro', n_fit, logF_fit, '-r')
hAxObj = handle(gca);
x_lim = get(hAxObj, 'XLim');
y_lim = get(hAxObj, 'YLim');
x_decades = log10(x_lim(2)/x_lim(1));
y_decades = log10(y_lim(2)/y_lim(1));
if x_decades >= y_decades % set x- and y-axis to be same size (so a = 1 is on first diagonal)
    y_lim_new = y_lim(1)*10^x_decades;
    set(hAxObj, 'YLim', [y_lim(1), y_lim_new]);
else
    x_lim_new = x_lim(1)*10^y_decades;
    set(hAxObj, 'XLim', [x_lim(1), x_lim_new]);
end
axis square
xlabel('log box size')
ylabel('log RMS fluctuations')
s1 = 'Figures/DFA/';
s2 = '_DFA.png';
s = strcat(s1,name);
s = strcat(s,s2);
saveas(gcf,s);

end