#!/bin/bash

# Set PYTHONPATH for Xinshuo_PyToolbox
export PYTHONPATH=${PYTHONPATH}:~/projects/AB3DMOT
export PYTHONPATH=${PYTHONPATH}:~/projects/AB3DMOT/Xinshuo_PyToolbox

# Run AB3DMOT on KITTI test split
python3 main.py --dataset KITTI --det_name pointrcnn --split test