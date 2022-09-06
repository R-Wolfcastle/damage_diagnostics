#!/bin/bash

#$ -cwd -V
#$ -l h_rt=40:00:00
#$ -l nodes=1,ppn=32

date
bash /resstore/b0133/eetss/BISICLES/diagnostic_damage_study/scripts/AIS/shell/run_executable.sh inputs.ais_inv_phi1
date

