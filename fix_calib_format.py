#!/usr/bin/env python3

import os
import glob

def fix_calib_file(filepath):
    """Fix calibration file format by adding missing colons"""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
            
        # If line doesn't contain ':' but starts with known keys, add it
        if ':' not in line:
            # Check if it starts with known calibration keys
            if line.startswith('R_rect '):
                line = line.replace('R_rect ', 'R0_rect: ', 1)
            elif line.startswith('Tr_velo_cam '):
                line = line.replace('Tr_velo_cam ', 'Tr_velo_to_cam: ', 1)
            elif line.startswith('Tr_imu_velo '):
                line = line.replace('Tr_imu_velo ', 'Tr_imu_to_velo: ', 1)
        
        fixed_lines.append(line + '\n')
    
    # Write back the fixed file
    with open(filepath, 'w') as f:
        f.writelines(fixed_lines)
    print(f"Fixed {filepath}")

def main():
    # Fix training calib files
    train_calib_dir = "~/projects/AB3DMOT/data/KITTI/tracking/training/calib"
    test_calib_dir = "~/projects/AB3DMOT/data/KITTI/tracking/testing/calib"
    
    for calib_dir in [train_calib_dir, test_calib_dir]:
        if os.path.exists(calib_dir):
            calib_files = glob.glob(os.path.join(calib_dir, "*.txt"))
            for calib_file in calib_files:
                fix_calib_file(calib_file)

if __name__ == "__main__":
    main()