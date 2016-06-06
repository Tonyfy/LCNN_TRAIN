#训练model的流程，适合有间断的训练，可以自动使用snapshot中最新的solverstate继续训练。
#1，从./snapshot中寻找日期最晚的一个*.solverstate
#2，caffe train的命令  加载上述solverstate 并进行训练

ls -l ./snapshot/*.*state -t >log.txt
snap=`head -1 log.txt|awk '{print $9}'`
nohup caffe train -solver="LCNN_solver.prototxt" -gpu=1 -snapshot=$snap &
