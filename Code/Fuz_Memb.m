% set the full path
fis = readfis('./testFuzzy/Fuzzy_rules/Fuzzy_3fac_939.fis');

raw_data = readmatrix('./testFuzzy/Fuzzy_table/Input_939.csv');
data = raw_data(:,2:4);

FM = evalfis(fis,data)

FM(:,4) = raw_data(:,1)
writematrix(FM,'./testFuzzy/Fuzzy_table/Output_939.csv')

%hold all
%plotmf(fis,'input',2)
%plot(82.52,1,'squre')
%plot(82.52,0,'squre')
%plot(477.6,1,'squre')
%plot(477.6,0,'squre')
%xline(82.52,'--')
%xline(477.6,'--')
%xticks([82.52 200 300 400 477.6 600])