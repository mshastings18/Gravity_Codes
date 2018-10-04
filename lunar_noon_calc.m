%% Calculating difference between lunar noon and lunar midnight

re = 6.378*10^6; % radius of earth (m)
rm = 3.8*10^8; % distance from center of earth to center of moon
mm = 7.3*10^22; % mass of the moon in kg
G = 6.67*10^-11; % Gravitational constant
% Force of gravity as a function of mass and distance
%      F = G(m1m2)/r^2
%      F = ma // so equilibrate forces and mass of the point is cancelled

% lunar noon, directly above so distance from center earth to moon - radius
% of earth
an = (G*(mm))/((rm - re)^2);

% lunar midnight, other side of earth. so distance to moon + radius of
% earth
am = (G*(mm))/((rm+re)^2);

% lunar noon is a decrease so negative change in gravity
delta_a = (am + an)*10^5  % need to put in mGals


%% Calculating difference in gravity between 600 Ma and present due to CA

g_pole = 9.861319102;

% g_phi = gpole - (angfreq^2)re

delta_p_perma = 18/4000 ; % change in period per ma
period = (24 - (delta_p_perma)*600)*60*60 % period 600Ma in secs
present_period = (24*60*60); % period today in seconds
w = (2*pi)/period; % angular freq 600Ma
wnow = (2*pi)/(present_period); % angular freq now

g_600 = g_pole - (w^2)*re*cosd(0)
g_now = g_pole - (wnow^2)*re*cosd(0)

delta_v = (g_now - g_600)*10^5 % change in mGals



%% Plotting Gravity functions

w = (2*pi)/(24*3600);
lat = [-90:1:90];
f = 1/298.257223563;
G = 6.67*10^-11;
Me = 5.972*10^24;
g_f = [];

r_lat = re*(1-f*(sind(abs(lat)).^2));
g_f = (G*Me)./(r_lat.^2);

g_lat = g_pole - (w^2)*re*cosd(abs(lat));
g_cum = g_f - (w^2)*re*cosd(abs(lat));

figure(1);
plot(lat, g_lat, 'color', 'r'); hold on;
plot(lat, g_f, 'color', 'b'); 
plot(lat, g_cum, 'color', 'g');
xlabel('Latitude (N)');
ylabel('Gravity (m/s/s)');
legend('G with Centripetal Acc', 'G with Flattening', 'G Cummulative', 'Location','SouthWest')
title('Gravity Functions')