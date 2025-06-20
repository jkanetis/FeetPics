% Load the CSV file with vertex coordinates and color data
csvFile = 'face_data_with_vertex_coords.csv';
data = readtable(csvFile);

% Initialize arrays for vertices and colors
faces = [];
vertices = [];
colors = [];

% Define normalized gray threshold
initialGray = [0.8, 0.8, 0.8];

% Iterate over each row in the data table
for i = 1:height(data)
    % Extract RGB color information and normalize to 0-1 range
    color = [data.Red(i), data.Green(i), data.Blue(i)];
    
    %test = (round(color * 100) / 100)
    
    % Check if the color is not gray
    if ~isequal(color, initialGray)  % Use rounding to avoid floating point precision issues
        % Parse the vertex coordinates
        coordStrings = split(data.Vertex_Coordinates{i}, '; ');
        numVertices = numel(coordStrings);
        faceIndices = zeros(1, numVertices);
    
        for j = 1:numVertices
            % Extract x, y, z from each coordinate string
            coordStr = coordStrings{j};
            coords = sscanf(coordStr, '(%f, %f, %f)');
            vertices = [vertices; coords'];
            faceIndices(j) = size(vertices, 1); % Index of the current vertex
        end
    
        % Append face indices and colors
        faces = [faces; faceIndices];
        colors = [colors; color];
    end
end

% Plot the mesh using patch
figure;
hold on;
for i = 1:size(faces, 1)
    % Get current face vertices and color
    faceVerts = vertices(faces(i, :), :);
    fill3(faceVerts(:, 1), faceVerts(:, 2), faceVerts(:, 3), colors(i, :), 'EdgeColor', 'none');
end
hold off;
axis equal;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('3D Mesh Visualization - Non-Gray Faces Only');