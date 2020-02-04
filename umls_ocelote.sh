#!/bin/bash
# Your job will use 1 node, 28 cores, and 168gb of memory total.
#PBS -q standard
#PBS -l select=1:ncpus=28:mem=168gb:pcmem=8gb
### Specify a name for the job
#PBS -N rnn_pretrained
### Specify the group name
#PBS -W group_list=nlp
### Used if job requires partial node only
#PBS -l place=pack:exclhost
### CPUtime required in hhh:mm:ss.
### Leading 0's can be omitted e.g 48:0:0 sets 48 hours
#PBS -l cput=336:00:00
### Walltime is how long your job will run
#PBS -l walltime=12:00:00
#PBS -e /home/u25/dongfangxu9/umls/log/error/twa_test
#PBS -o /home/u25/dongfangxu9/umls/log/output/twa_test

#####module load cuda80/neuralnet/6/6.0
#####module load cuda80/toolkit/8.0.61
module load singularity/3.2.1

cd $PBS_O_WORKDIR

singularity exec --nv /extra/dongfangxu9/image_bert/hpc-ml_centos7-python37.sif python3.7
