#!/bin/bash

# Set PYTHONPATH for Xinshuo_PyToolbox
export PYTHONPATH=${PYTHONPATH}:/home/antonin-sumner/projects/AB3DMOT
export PYTHONPATH=${PYTHONPATH}:/home/antonin-sumner/projects/AB3DMOT/Xinshuo_PyToolbox

# Run AB3DMOT on KITTI val split
python3 main.py --dataset KITTI --det_name pointrcnn --split val