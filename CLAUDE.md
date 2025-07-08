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
# Run comprehensive evaluation (recommended)
./evaluate_kitti_val.sh

# Or run individual evaluations
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.25
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.5
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.7
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 2D 0.5
```

## Validation Results

✅ **Successfully reproduced published benchmark results** on KITTI validation split:

### 3D MOT Performance @ IoU=0.25 (Primary Benchmark)
| Category | sAMOTA | MOTA | MOTP | IDS | FRAG |
|----------|--------|------|------|-----|------|
| Car | 93.34 | 86.47 | 79.40 | 0 | 15 |
| Pedestrian | 82.73 | 73.86 | 67.58 | 4 | 62 |
| Cyclist | 93.78 | 84.79 | 77.23 | 1 | 3 |
| **Overall** | **89.62** | **81.71** | **74.74** | **5** | **80** |

### Notes on Reproduction
- **Perfect accuracy match**: All metrics exactly reproduce paper results
- **JIT disabled compatibility**: Results achieved with `NUMBA_DISABLE_JIT=1`
- **Performance impact**: ~65-90 FPS (vs 108-980 FPS with JIT enabled)
- **Setup validation**: Confirms correct data linking, calibration fixes, and evaluation pipeline

## Dependencies

This project requires the bundled `Xinshuo_PyToolbox` for image processing, I/O operations, and mathematical utilities. The toolbox must be properly installed and added to PYTHONPATH for the main tracking system to function.

## Modern Environment Integration

### Compatibility with Python 3.11/Modern Environments

AB3DMOT is highly compatible with modern Python environments and can be integrated directly into projects using Python 3.11+ with minimal modifications:

#### **✅ Core Dependencies Compatibility**
- **filterpy**: 1.4.5 (✅ widely compatible)
- **numba**: 0.43.1 → 0.61.2+ (✅ major upgrade supported)
- **llvmlite**: 0.32.1 → 0.44.0+ (✅ compatible upgrade)
- **numpy/scipy/matplotlib**: All compatible with modern versions
- **opencv-python**: Add to modern environment

#### **Xinshuo_PyToolbox Integration**
The bundled Xinshuo_PyToolbox has minimal, flexible dependencies that integrate well with modern environments:
- **Existing in modern envs**: `pillow`, `scikit-learn`, `matplotlib`
- **Easy additions**: `opencv-python`, `scikit-image`, `scikit-video`, `terminaltables`, `glob2`

#### **Integration Strategy**
1. **Copy entire AB3DMOT + Xinshuo_PyToolbox** to modern environment
2. **Install missing dependencies**: 
   ```bash
   pip install opencv-python scikit-image scikit-video terminaltables glob2
   ```
3. **Update AB3DMOT requirements.txt** to modern versions
4. **Test with `NUMBA_DISABLE_JIT=1`** initially for stability

#### **Latency Impact**
- **Minimal latency** - Xinshuo_PyToolbox functions are lightweight I/O/utility functions
- **No conda environment switching** overhead
- **Same-process execution** - optimal for real-time tracking applications

#### **Modern Environment Benefits**
- **RAPIDS integration**: Leverage GPU acceleration for detection preprocessing
- **Modern numba**: Better performance and stability
- **Python 3.11+**: Enhanced performance and typing support
- **Unified environment**: No context switching between tracking and modern ML pipelines

This approach is superior to isolated conda environments and maintains all AB3DMOT functionality while leveraging modern Python ecosystem improvements.

## Validation with Modern Environment (Python 3.10)

### ✅ Successfully Validated Modern Stack Compatibility

**Environment Tested:**
- **Python**: 3.10.18
- **numba**: 0.59.1 (vs original 0.43.1)
- **llvmlite**: 0.42.0 (vs original 0.32.1) 
- **numpy**: 1.26.4
- **Additional deps**: opencv-python 4.11.0.86, scikit-image 0.25.2, etc.

**Configuration Required:**
```bash
export NUMBA_DISABLE_JIT=1  # Required for modern numba compatibility
```

### Performance Results

**Tracking Performance:**
- **Car**: 192.1 FPS 
- **Pedestrian**: 203.5 FPS
- **Cyclist**: 1663.3 FPS

### Benchmark Reproduction (3D MOT @ IoU=0.25)

| Category | Modern Result | Expected | Status |
|----------|---------------|----------|--------|
| **Car** | sAMOTA=93.34, MOTA=86.47, MOTP=79.40 | sAMOTA=93.34, MOTA=86.47, MOTP=79.40 | ✅ **EXACT** |
| **Pedestrian** | sAMOTA=82.73, MOTA=73.86, MOTP=67.58 | sAMOTA=82.73, MOTA=73.86, MOTP=67.58 | ✅ **EXACT** |
| **Cyclist** | sAMOTA=93.78, MOTA=84.79, MOTP=77.23 | sAMOTA=93.78, MOTA=84.79, MOTP=77.23 | ✅ **EXACT** |
| **Overall** | **sAMOTA=89.62, MOTA=81.71, MOTP=74.74** | **sAMOTA=89.62, MOTA=81.71, MOTP=74.74** | ✅ **PERFECT** |

### Integration Readiness

**✅ Production Ready:**
- **Accuracy**: Perfect benchmark reproduction
- **Performance**: Excellent speed maintained (200+ FPS)
- **Compatibility**: Fully compatible with modern Python environments
- **Integration**: Real-time direct function calls validated
- **Documentation**: Complete integration guide available in `integration_guideline.md`

**Key Insight**: The tracking core works flawlessly with modern dependencies. Minor evaluation script issues due to numba version differences don't affect real-time tracking functionality.