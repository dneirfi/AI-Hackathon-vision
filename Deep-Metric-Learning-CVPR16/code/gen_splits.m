function gen_splits

conf = config;

% conf.root_path = '/scail/scratch/group/cvgl/hsong/Deep-Lifting-for-Metric-Learning-CVPR/code/ebay/';
% conf.cache_path = '/scail/scratch/group/cvgl/hsong/Deep-Lifting-for-Metric-Learning-CVPR/code/ebay/cache';
% conf.image_path = '/cvgl/group/Ebay_Dataset/';

%% generate splits
[image_ids, class_ids, superclass_ids, path_list] = ...
    textread('/cvgl/group/Ebay_Dataset/Ebay_train.txt', '%d %d %d %s',...
    'headerlines', 1);

train_images = {};
dict = containers.Map('keytype', 'double', 'valuetype', 'any');

for i = 1:length(image_ids)
    imageid = image_ids(i);
    classid = class_ids(i);
    filename = path_list{i};
    
    fprintf('%d/%d, classid= %d, filename= %s\n', ...
        i, length(image_ids), classid, filename);
    
    train_images{end+1} = filename;
    
    % hash it
    if isKey(dict, classid)
        dict(classid) = [dict(classid), imageid];
    else
        dict(classid) = [imageid];
    end
end
   
[image_ids, class_ids, superclass_ids, path_list] = ...
    textread('/cvgl/group/Ebay_Dataset/Ebay_test.txt', '%d %d %d %s',...
    'headerlines', 1);

val_images = {};
for i = 1:length(image_ids)
    imageid = image_ids(i);
    classid = class_ids(i);
    filename = path_list{i};
    
    fprintf('%d/%d, classid= %d, filename= %s\n', ...
        i, length(image_ids), classid, filename);
    
    val_images{end+1} = filename;
    
    % hash it
    if isKey(dict, classid)
        dict(classid) = [dict(classid), imageid];
    else
        dict(classid) = [imageid];
    end
end
    
savepath = [conf.root_path, 'splits.mat'];
save(savepath, 'train_images', 'val_images', 'dict');