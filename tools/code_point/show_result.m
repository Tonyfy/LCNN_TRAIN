clear all
close all
clc

fid = fopen('result0.bin', 'rb');
imageNum = fread(fid, 1, 'int32');
pointNum = fread(fid, 1, 'int32');
assert(pointNum == 5);
valid = fread(fid, imageNum, 'int8');
assert(all(valid) == 1);
point = reshape(fread(fid, 2 * pointNum * imageNum, 'float64'), [2 * pointNum, imageNum])';
fclose(fid);

green(1, 1, :) = [0 255 0];
mkdir('show_result0');
mkdir('image0');

fid = fopen('bbox0.txt', 'r');
for n1 = 1 : imageNum
    imageName = fscanf(fid, '%s', 1);
    fscanf(fid, '%d', 4);
    I = imread(['../code_face/image/' imageName]);
    if size(I, 3) == 1
        I = repmat(I, [1 1 3]);
    end
    imwrite(I, ['image0/' imageName]);
    pt = point(n1, :);
    pt = round(pt) + 1;
    for n2 = 1 : pointNum
        p = pt(n2 * 2 - 1 : n2 * 2);
        I(p(2) - 1 : p(2) + 1, p(1) - 2 : p(1) + 2, :) = repmat(green, [3 5]);
        I([p(2) - 2 p(2) + 2], p(1) - 1 : p(1) + 1, :) = repmat(green, [2 3]);
    end
    imwrite(I, ['show_result0/' imageName]);

end
fclose(fid);
