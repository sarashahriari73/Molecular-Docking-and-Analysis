#!/bin/bash

export LC_NUMERIC=en_US.UTF-8

awk '{sum+=$4; sum2+=$4*$4} END {print sum/NR, "+-", sqrt(sum2/NR-(sum/NR)^2)}' energies.dat


