#!/bin/bash
export NUMBA_DISABLE_JIT=1
echo "NUMBA JIT DISABLED"
# Set PYTHONPATH for Xinshuo_PyToolbox
export PYTHONPATH=${PYTHONPATH}:~/projects/AB3DMOT
export PYTHONPATH=${PYTHONPATH}:~/projects/AB3DMOT/Xinshuo_PyToolbox

echo "============================================="
echo "EVALUATING AB3DMOT ON KITTI VALIDATION SET"
echo "============================================="
echo ""

echo "📊 Running 3D MOT evaluation with IoU threshold 0.25..."
echo "Expected benchmark results (from paper):"
echo "  Car:        sAMOTA=93.34, MOTA=86.47, MOTP=79.40"
echo "  Pedestrian: sAMOTA=82.73, MOTA=73.86, MOTP=67.58"
echo "  Cyclist:    sAMOTA=93.78, MOTA=84.79, MOTP=77.23"
echo "  Overall:    sAMOTA=89.62, MOTA=81.71, MOTP=74.74"
echo ""
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.25
echo ""

echo "📊 Running 3D MOT evaluation with IoU threshold 0.5..."
echo "Expected benchmark results (from paper):"
echo "  Car:        sAMOTA=92.57, MOTA=84.81, MOTP=79.82"
echo "  Pedestrian: sAMOTA=77.68, MOTA=68.19, MOTP=68.55"
echo "  Cyclist:    sAMOTA=92.05, MOTA=83.38, MOTP=77.52"
echo "  Overall:    sAMOTA=87.43, MOTA=78.79, MOTP=75.30"
echo ""
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.5
echo ""

echo "📊 Running 3D MOT evaluation with IoU threshold 0.7..."
echo "Expected benchmark results (from paper):"
echo "  Car:        sAMOTA=74.96, MOTA=62.48, MOTP=82.64"
echo ""
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 3D 0.7
echo ""

echo "📊 Running 2D MOT evaluation with IoU threshold 0.5..."
echo "Expected benchmark results (from paper):"
echo "  Car:        sAMOTA=93.08, MOTA=85.98, MOTP=86.95"
echo "  Pedestrian: sAMOTA=69.70, MOTA=60.41, MOTP=67.18"
echo "  Cyclist:    sAMOTA=91.62, MOTA=83.01, MOTP=85.55"
echo "  Overall:    sAMOTA=84.80, MOTA=76.47, MOTP=79.89"
echo ""
python3 scripts/KITTI/evaluate.py pointrcnn_val_H1 1 2D 0.5
echo ""

echo "✅ Evaluation completed!"
echo ""
echo "📝 Notes:"
echo "  - Performance differences may occur due to NUMBA_DISABLE_JIT=1"
echo "  - Paper results were obtained with JIT compilation enabled"
echo "  - Slight variations are expected across different hardware/environments"