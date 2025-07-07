# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AB3DMOT is a 3D Multi-Object Tracking baseline system that works with KITTI and nuScenes datasets. The system combines 3D Kalman filtering with Hungarian algorithm for state estimation and data association in autonomous driving scenarios.

## Key Architecture Components

### Core Tracking System
- **AB3DMOT_libs/model.py**: Main tracking class `AB3DMOT` that orchestrates the entire tracking pipeline
- **AB3DMOT_libs/kalman_filter.py**: Kalman filter implementation for state estimation (10D state: x,y,z,theta,l,w,h,dx,dy,dz)
- **AB3DMOT_libs/matching.py**: Data association algorithms (Hungarian/Greedy matching with various distance metrics)
- **AB3DMOT_libs/dist_metrics.py**: Distance metrics for object association (IoU, 3D distance, ground distance)

### Data Processing Pipeline
- **AB3DMOT_libs/io.py**: Data loading and saving utilities for detections and tracking results
- **AB3DMOT_libs/box.py**: 3D bounding box operations and transformations
- **AB3DMOT_libs/utils.py**: Configuration management and utility functions

### Dataset Support
- **AB3DMOT_libs/kitti_*.py**: KITTI dataset specific utilities (calibration, objects, tracking format)
- **AB3DMOT_libs/nuScenes_*.py**: nuScenes dataset utilities and format conversion

## Common Commands

### Main Tracking Execution
```bash
# Run tracking on KITTI dataset
python3 main.py --dataset KITTI --split val --det_name pointrcnn

# Run tracking on nuScenes dataset  
python3 main.py --dataset nuScenes --split val --det_name centerpoint
```

### Post-Processing and Evaluation
```bash
# Apply confidence thresholding to tracking results
python3 scripts/post_processing/trk_conf_threshold.py --dataset KITTI --result_sha pointrcnn_val_H1

# Visualize tracking results
python3 scripts/post_processing/visualization.py --result_sha pointrcnn_val_H1_thres --split val

# Evaluate tracking performance on KITTI
python3 scripts/KITTI/evaluate.py

# Evaluate tracking performance on nuScenes
python3 scripts/nuScenes/evaluate.py
```

### Environment Setup
```bash
# Install dependencies
pip3 install -r requirements.txt

# Set up Xinshuo_PyToolbox (required dependency)
cd Xinshuo_PyToolbox
pip3 install -r requirements.txt
cd ..

# Add to PYTHONPATH (required for imports)
export PYTHONPATH=${PYTHONPATH}:/path/to/AB3DMOT
export PYTHONPATH=${PYTHONPATH}:/path/to/AB3DMOT/Xinshuo_PyToolbox

# Fix calibration file format (required for KITTI)
python3 fix_calib_format.py

# Disable numba JIT if experiencing segmentation faults
export NUMBA_DISABLE_JIT=1
```

## Configuration System

### Dataset Configurations
- **configs/KITTI.yml**: KITTI-specific parameters (pointrcnn/pvrcnn detectors, Car/Pedestrian/Cyclist categories)
- **configs/nuScenes.yml**: nuScenes-specific parameters (centerpoint/megvii detectors, 7 object categories)

### Key Parameters
- `ego_com`: Enable ego-motion compensation for better tracking
- `num_hypo`: Number of tracking hypotheses (usually 1)
- `score_threshold`: Detection confidence filtering threshold
- Category-specific tuning in `model.py:get_param()` for optimal performance per detector/dataset

## Data Directory Structure

```
data/
├── KITTI/
│   ├── detection/          # Detection results from various detectors
│   └── tracking/           # Ground truth tracking labels
└── nuScenes/
    ├── detection/          # Detection results 
    └── nuKITTI/           # Converted nuScenes data in KITTI format
```

## Results and Output

- **results/**: Main output directory containing tracking results
- **results/{dataset}/{detector}_{category}_{split}_H{num_hypo}/**: Tracking results per configuration
- **data_{hypo_index}/**: Individual hypothesis results for multi-hypothesis tracking
- **log/**: Execution logs with timing and performance metrics

## Testing and Validation

The system uses a detection-based validation approach:
1. Load pre-computed 3D detections from supported detectors
2. Apply tracking algorithm with dataset/detector-specific parameters
3. Evaluate using official KITTI/nuScenes metrics
4. Post-process results with confidence thresholding and visualization

### Quick Setup Scripts
- **run_kitti_test_fixed.sh**: Run tracking on KITTI test split with JIT disabled
- **run_kitti_val_fixed.sh**: Run tracking on KITTI validation split with JIT disabled  
- **fix_calib_format.py**: Fix KITTI calibration file format (adds missing colons)

### KITTI Data Setup
Create symbolic links to your KITTI data:
```bash
mkdir -p data/KITTI/tracking/training data/KITTI/tracking/testing
# Link training data
cd data/KITTI/tracking/training
ln -sf /path/to/KITTI_MOT/data_tracking_calib/training/calib calib
ln -sf /path/to/KITTI_MOT/data_tracking_image_2/training/image_02 image_02
ln -sf /path/to/KITTI_MOT/data_tracking_label_2/training/label_02 label_02
ln -sf /path/to/KITTI_MOT/data_tracking_oxts/training/oxts oxts
ln -sf /path/to/KITTI_MOT/data_tracking_velodyne/training/velodyne velodyne
# Link testing data (similar pattern)
```

### KITTI Evaluation Commands
```bash
# 3D MOT evaluation with different IoU thresholds
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.25
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.5
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.7

# 2D MOT evaluation
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 2D 0.5
```

## Dependencies

This project requires the bundled `Xinshuo_PyToolbox` for image processing, I/O operations, and mathematical utilities. The toolbox must be properly installed and added to PYTHONPATH for the main tracking system to function.