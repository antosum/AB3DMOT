#!/bin/bash

# Disable numba JIT to avoid segfault
export NUMBA_DISABLE_JIT=1

# Set PYTHONPATH for Xinshuo_PyToolbox
export PYTHONPATH=${PYTHONPATH}:/home/antonin-sumner/projects/AB3DMOT
export PYTHONPATH=${PYTHONPATH}:/home/antonin-sumner/projects/AB3DMOT/Xinshuo_PyToolbox

# Run AB3DMOT on KITTI validation split
echo "Running AB3DMOT on KITTI validation split..."
echo "Processing validation sequences: 0001, 0006, 0008, 0010, 0012, 0013, 0014, 0015, 0016, 0018, 0019"
python3 main.py --dataset KITTI --det_name pointrcnn --split val