#!/bin/bash

#$ -cwd -V
#$ -l h_rt=00:05:00
#$ -pe smp 8
#$ -l h_vmem=12G

date
bash /resstore/b0133/eetss/BISICLES/diagnostic_damage_study/scripts/AIS/shell/forward/run_executable.sh /resstore/b0133/eetss/BISICLES/diagnostic_damage_study/scripts/AIS/control_files/forward/inputs_ais_thermo_fwd_2km
date

