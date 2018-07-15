% srcroot = 'E:/Lishi/baseline/Feature_DPN107';
% dstroot = 'E:/Lishi/baseline/Feature_DPN107/yml';
% srcroot = 'E:/Lishi/Datasets/5-Features/COCO_feat';
% dstroot = 'E:/Lishi/baseline/COCO/yml';

srcroot = 'E:/Lishi/AAAI2018/baseline/Feature_DPN107_40/part_2';
dstroot = 'E:/Lishi/AAAI2018/baseline/Feature_DPN107_40/yml/part_2';

if ~exist(dstroot,'dir')
    mkdir(dstroot);
end
filelists = dir([srcroot filesep '*.mat']);
num_files=numel(filelists);

for i = 1:num_files
    fprintf('start deal with the number: %d|%d\n',i,num_files);
    filename = fullfile(srcroot,filelists(i).name);
    [~,name,~] = fileparts(filename);
    destfile = fullfile(dstroot,[name '.yml']);
    feat_matrix = importdata(filename);
    dym_matlab2opencv(feat_matrix,destfile,'w');
end