#!/bin/bash

#$ -cwd -V
#$ -l h_rt=02:30:00
#$ -pe smp 8
#$ -l h_vmem=12G

date
bash /resstore/b0133/eetss/BISICLES/diagnostic_damage_study/scripts/AIS/shell/adjoint/run_executable.sh /resstore/b0133/eetss/BISICLES/diagnostic_damage_study/scripts/AIS/control_files/adjoint/inputs.ais_adj_2km
date

