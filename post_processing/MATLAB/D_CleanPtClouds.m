% Clean Point Clouds
% Drew Davey
% Last updated: 2024-03-17 

clear; clc; close all;

%% Inputs

path = uigetdir('../../','Select path to session to clean ptClouds'); % load path to dir to clean ptClouds
path = [path '/mats'];
if ~exist(path, 'dir')
    disp('No mats/ directory in this session.');
end

cleanFlag = 0; % Set to 1 for manual point cloud editing, or 0 for automatic cleaning

bounds = [-5 5 -5 5 0 30];   % [xmin xmax ymin ymax zmin zmax] for trimming points (meters)

binSize = 1;    % size of the cubic bin for stepping through points (meters)

%% Process ptClouds
    
% Get all .mat files in the path
matFiles = dir(fullfile(path, '*.mat'));

% Loop through each .mat file
for i = 1:length(matFiles)
    matFile = fullfile(path, matFiles(i).name);
    fprintf('Processing file: %s\n', matFile);
    
    % Load points3D and ptCloud
    load(matFile);

    % Reshape points3D and J1 into M-by-3 format
    [rows, cols, ~] = size(points3D);  % Get the dimensions
    points3D_reshaped = reshape(points3D, [], 3);  % Reshape to M-by-3
    J1_reshaped = reshape(J1, [], 3);  % Reshape color to M-by-3

    % Save previous versions with timestamp before applying changes
    timestamp = datestr(now, 'yyyymmdd_HHMMSS');
    
    % Create new variable names with timestamps
    eval(['points3D_', timestamp, ' = points3D;']);
    eval(['ptCloud_', timestamp, ' = ptCloud;']);
    
    % Save timestamped variables to the mat file
    save(matFile, ['points3D_', timestamp], ['ptCloud_', timestamp], '-append');
    

    % Apply QA/QC techniques here
    points3D_cleaned = trimBounds(points3D_reshaped, bounds, binSize); % Update points3D after QA/QC
    ptCloud = pointCloud(points3D_cleaned, 'Color', J1_reshaped(1:size(points3D_cleaned, 1), :)); % Create the new point cloud

%     % Apply QA/QC techniques here
%     points3D = trimBounds(points3D, bounds, binSize); % Update points3D after QA/QC
%     ptCloud = pointCloud(points3D, Color=J1);

    % If cleanFlag is set, manually edit the point cloud using the brush tool
    if cleanFlag
        title('Use the brush tool to manually clean the point cloud');
        h = uicontrol('Style', 'pushbutton', 'String', 'Finish Editing', ...
                      'Position', [20 20 100 40], 'Callback', 'uiresume(gcbf)');
        uiwait(gcf); % Wait for user to finish editing

        % Re-save after manual editing
        points3D = ptCloud.Location; % Extract manually cleaned points3D
        save(matFile, 'points3D', 'ptCloud', '-append');
        ptCloud = pointCloud(points3D, Color=J1);   % Recreate ptCloud from updated points3D
    end
    
    % Save updated points3D and ptCloud
    save(matFile, 'points3D', 'ptCloud', '-append');
    
end

%% QA/QC Functions

function points3D_cleaned = trimBounds(points3D, bounds, binSize)
    
    % Get the min and max values of the points3D for safety
    xMinPts = min(points3D(:,1));
    xMaxPts = max(points3D(:,1));
    yMinPts = min(points3D(:,2));
    yMaxPts = max(points3D(:,2));
    zMinPts = min(points3D(:,3));
    zMaxPts = max(points3D(:,3));
    
    % Ensure the bounds are within the actual limits of the point cloud
    bounds(1) = max(bounds(1), xMinPts); % xmin
    bounds(2) = min(bounds(2), xMaxPts); % xmax
    bounds(3) = max(bounds(3), yMinPts); % ymin
    bounds(4) = min(bounds(4), yMaxPts); % ymax
    bounds(5) = max(bounds(5), zMinPts); % zmin
    bounds(6) = min(bounds(6), zMaxPts); % zmax
    
    % Trim points to the specified bounds
    x = points3D(:,1);
    y = points3D(:,2);
    z = points3D(:,3);
    
    % Apply bounds to keep only the points within specified ranges
    withinBounds = (x >= bounds(1) & x <= bounds(2)) & ...
                   (y >= bounds(3) & y <= bounds(4)) & ...
                   (z >= bounds(5) & z <= bounds(6));
    
    points3D = points3D(withinBounds, :);
    
    % Now step through the points cubically in bins of size binSize
    xMin = bounds(1); xMax = bounds(2);
    yMin = bounds(3); yMax = bounds(4);
    zMin = bounds(5); zMax = bounds(6);
    
    points3D_cleaned = [];
    
    for xStart = xMin:binSize:xMax
        for yStart = yMin:binSize:yMax
            for zStart = zMin:binSize:zMax
                % Define the current bin
                xEnd = xStart + binSize;
                yEnd = yStart + binSize;
                zEnd = zStart + binSize;
                
                % Find points within this bin
                inBin = (points3D(:,1) >= xStart & points3D(:,1) < xEnd) & ...
                        (points3D(:,2) >= yStart & points3D(:,2) < yEnd) & ...
                        (points3D(:,3) >= zStart & points3D(:,3) < zEnd);
                
                binPoints = points3D(inBin, :);
                
                if ~isempty(binPoints)
                    % Compute the mean and standard deviation for each dimension
                    binMean = mean(binPoints, 1);
                    binStd = std(binPoints, 1);
                    
                    % Find points within 3 standard deviations of the mean
                    deviationFromMean = abs(binPoints - binMean);
                    within3Std = all(deviationFromMean <= 3 * binStd, 2);
                    
                    % Add the cleaned points for this bin to the final output
                    points3D_cleaned = [points3D_cleaned; binPoints(within3Std, :)]; %#ok<AGROW>
                end
            end
        end
    end
end




