#!/bin/bash

#$ -cwd -V
#$ -l h_rt=20:00:00
#$ -pe smp 16
#$ -l h_vmem=5G

inputs_file=$1
echo ${inputs_file}

date
bash /resstore/b0133/eetss/BISICLES/diagnostic_damage_study/scripts/AIS/shell/run_executable_nopetsc.sh ${inputs_file}
date

