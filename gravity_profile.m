
g = grav_profile(1000000, 10, -25, 25);


function [gz1] = grav_profile(mass, depth, xmin, xmax)
    % calculate gravity along profile of point mass at depth. Mass must be
    % in kilograms and depth must be in meters. xmin and xmax constrain the
    % domains of the profile you would like to make. Note that the mass is
    % centered at x=0
    
    G = 6.67e-11; % Gravitational constant m^3/(kg*s^2)
    mp1 = mass; % kg
    mp2 = mp1*2
    mp3 = mp1*3
    z1 = depth; % m
    z2 = depth + 5; % same mass at deeper depth
    z3 = depth - 5; % same mass at shallower depth
    z0 = 0; % surface
    x = [xmin:1:xmax]; % x domain in meters
    x0 = 0; % x position of the mass
    
    % depth z1
    g_top = G*mp2*(z1-z0);
    g_bottom = ((x.^2) + z1^2).^(3/2);
    
    g = g_top./g_bottom; % in m/s/s
    
    gz1 = g.*1e5; % convert to mGals
    
    % depth z2
    g_top = G*mp3*(z2-z0);
    g_bottom = ((x.^2) + z2^2).^(3/2);
    
    g = g_top./g_bottom; % in m/s/s
    
    gz2 = g.*1e5; % convert to mGals
    
    
    % depth z3
    g_top = G*mp1*(z3-z0);
    g_bottom = ((x.^2) + z3^2).^(3/2);
    
    g = g_top./g_bottom; % in m/s/s
    
    gz3 = g.*1e5; % convert to mGals
    
    figure(1)
    subplot(2,1,1)
    plot(x, gz1,'--r', x, gz2,'--b', x, gz3,'--g','LineWidth',1.5);
    title('Gravity Anomaly Due to Point Mass')
    ylabel('Gravity (mGals)');
    xlabel('Position Along Profile (m)');
    
    subplot(2,1,2)
    plot(x0, -z3, 'og', 'Markersize', 10, 'MarkerFaceColor', 'g')
    hold on;
    plot(x0, -z1, 'or', 'Markersize', 10, 'MarkerFaceColor', 'r')
    plot(x0, -z2, 'ob', 'Markersize', 10, 'MarkerFaceColor', 'b')
    hold off;
    axis([min(x) max(x) -2*depth 0]);
    legend('m = 1,000,000 kg', 'm = 2,000,000 kg', 'm = 3,000,000 kg');
    ylabel('Depth (m)')
    xlabel('Position Along Profile (m)')
    
end