% load　roc.txt and draw the performance on lfw.
clc;cla;clear;
roc = load('roc.txt');
posAcceptrate = roc(:,2);
negRejectrate = roc(:,3);
plot(posAcceptrate,negRejectrate,'b.-');
title('模型在lfw库上的性能表现');
xlabel('负样本拒识率');
ylabel('正样本通过率');