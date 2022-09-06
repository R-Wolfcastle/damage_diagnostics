#!/bin/bash

#$ -cwd -V
#$ -l h_rt=00:15:00
#$ -pe smp 8
#$ -l h_vmem=12G

date
bash /resstore/b0133/eetss/BISICLES/diagnostic_damage_study/scripts/AIS/shell/run_executable.sh inputs.ais_inv_phi1
date

