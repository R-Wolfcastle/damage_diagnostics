#!/bin/bash

# Arguments:
# $1: inputs file

#. /nobackup/eetss/BISICLES/.bstart_petsc
#driver=$BISICLES_HOME/BISICLES/code/exec2D/driver2d.Linux.64.mpic++.mpif90.DEBUG.OPT.MPI.PETSC.ex
. /nobackup/eetss/BISICLES/.bstart
driver=$BISICLES_HOME/BISICLES/code/exec2D/driver2d.Linux.64.mpic++.gfortran.DEBUG.OPT.MPI.ex

mpirun $driver $1

