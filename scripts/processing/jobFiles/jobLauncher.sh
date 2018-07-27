#!/bin/sh
#SBATCH --job-name=jobLauncher
#SBATCH --output OutJL.out
#SBATCH --error ErrBN.err
#SBATCH -n 10
#SBATCH -N 1

module load intel
module load python3/anaconda/5.0.1
