clc; clear;
M = readtable('C:\Users\RayWong\Desktop\gps_address.csv');
M = table2array(M);

kmlwriteline('C:\Users\RayWong\Desktop\gps.kml', M(:,1), M(:,2),M(:,3),...
        'Color','r', 'LineWidth', 5)
