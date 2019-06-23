#!/bin/bash

#PBS -lwalltime=25:00:00
#PBS -lnodes=1:ppn=1
#PBS -W group_list=ndssl
#PBS -q ndssl_q
#PBS -j oe
#PBS -o pbs.log

## Calculate the number of processors requested so we can
## automatically fill in the "np" parameter for mpirun commands

cd $PBS_O_WORKDIR

NUM_PROCS=`/bin/cat $PBS_NODEFILE | /usr/bin/wc -l | /bin/sed "s/  //g"`
. /etc/profile.d/modules.sh
module add ndssl/networkx/1.6

for f in /home/gkorkmaz/git/iarpa_embers/code/twitt*
do
    python /home/gkorkmaz/git/iarpa_embers/code/consolidateScores.py /home/gkorkmaz/git/iarpa_embers/code/hashtags.txt "$f" "/home/gkorkmaz/git/iarpa_embers/code/${f:73}-cons"
done
