function matlab2opencv_int( variable, fileName, flag)

[rows cols] = size(variable);

% Beware of Matlab's linear indexing
variable = variable';

% Write mode as default
if ( ~exist('flag','var') )
    flag = 'w';
end

if ( ~exist(fileName,'file') || flag == 'w' )
    % New file or write mode specified
    file = fopen( fileName, 'w');
    fprintf( file, '%%YAML:1.0\n');
else
    % Append mode
    file = fopen( fileName, 'a');
end

% Write variable header
fprintf( file, '    %s: !!opencv-matrix\n', inputname(1));
fprintf( file, '        rows: %d\n', rows);
fprintf( file, '        cols: %d\n', cols);
fprintf( file, '        dt: i\n');
fprintf( file, '        data: [ ');

% Write variable data
for i=1:rows*cols
    fprintf( file, '%i', variable(i));
    if (i == rows*cols), break, end
    fprintf( file, ', ');
    if mod(i+1,8) == 0
        fprintf( file, '\n            ');
    end
end

fprintf( file, ']\n');

fclose(file);

