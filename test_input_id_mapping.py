#!/usr/bin/env python3
"""
Test script to demonstrate input bbox ID preservation in AB3DMOT

This script shows how to use the new input_ids parameter to track
the correspondence between input bounding boxes and output tracklets.
"""

import numpy as np
import sys
import os

# Add AB3DMOT to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from AB3DMOT_libs.model import AB3DMOT
from AB3DMOT_libs.utils import Config

def create_sample_detections():
    """Create sample detections for testing"""
    # Format: [h, w, l, x, y, z, theta]
    detections = np.array([
        [1.5, 1.8, 4.2, 10.0, 0.0, 0.0, 0.1],  # Car 1
        [1.7, 2.0, 4.5, 15.0, 5.0, 0.0, 0.3],  # Car 2  
        [1.6, 1.9, 4.0, 8.0, -3.0, 0.0, -0.2], # Car 3
    ])
    
    # Sample info array (dummy confidence scores)
    info = np.array([
        [0.9],
        [0.8], 
        [0.85]
    ])
    
    return detections, info

def test_input_id_mapping():
    """Test the input ID mapping functionality"""
    
    print("=== AB3DMOT Input ID Mapping Test ===\n")
    
    # Create a simple config
    cfg = Config()
    cfg.dataset = 'KITTI'
    cfg.det_name = 'pointrcnn'
    cfg.vis = False
    cfg.ego_com = False
    cfg.affi_pro = False
    
    # Initialize tracker
    tracker = AB3DMOT(cfg, cat='Car')
    
    # Frame 1: Initial detections
    print("Frame 1: Initial detections")
    dets1, info1 = create_sample_detections()
    input_ids1 = [100, 200, 300]  # Your original bbox IDs
    
    print(f"Input detections: {len(dets1)}")
    print(f"Input IDs: {input_ids1}")
    
    results1, affi1, id_mapping1 = tracker.track(
        {'dets': dets1, 'info': info1}, 
        frame=0, 
        seq_name='test',
        input_ids=input_ids1
    )
    
    print(f"Output tracks: {len(results1[0])}")
    if len(results1[0]) > 0:
        track_ids1 = results1[0][:, 7].astype(int).tolist()
        print(f"Track IDs: {track_ids1}")
    else:
        track_ids1 = []
    print(f"ID Mapping: {id_mapping1}")
    print()
    
    # Frame 2: Some detections moved, one new detection
    print("Frame 2: Some detections moved, one new")
    dets2 = np.array([
        [1.5, 1.8, 4.2, 11.0, 0.5, 0.0, 0.1],  # Car 1 moved (ID 100)
        [1.6, 1.9, 4.0, 7.5, -2.8, 0.0, -0.2], # Car 3 moved (ID 300)  
        [1.4, 1.7, 3.8, 20.0, 8.0, 0.0, 0.0],  # New car (ID 400)
    ])
    info2 = np.array([[0.9], [0.85], [0.7]])
    input_ids2 = [100, 300, 400]  # Note: ID 200 disappeared, 400 is new
    
    print(f"Input detections: {len(dets2)}")
    print(f"Input IDs: {input_ids2}")
    
    results2, affi2, id_mapping2 = tracker.track(
        {'dets': dets2, 'info': info2}, 
        frame=1, 
        seq_name='test',
        input_ids=input_ids2
    )
    
    print(f"Output tracks: {len(results2[0])}")
    if len(results2[0]) > 0:
        track_ids2 = results2[0][:, 7].astype(int).tolist()
        print(f"Track IDs: {track_ids2}")
    else:
        track_ids2 = []
    print(f"ID Mapping: {id_mapping2}")
    print()
    
    # Demonstrate the mapping utility
    print("=== ID Mapping Analysis ===")
    print("This mapping tells you:")
    for track_id, input_id in id_mapping2.items():
        if input_id is not None:
            print(f"  Track {track_id} corresponds to your input bbox {input_id}")
        else:
            print(f"  Track {track_id} is propagated from previous frame (no current detection)")
    
    print("\n=== Test Complete ===")
    print("The AB3DMOT tracker now preserves input bbox IDs!")
    print("You can use the id_mapping to match output tracklets with your input bboxes.")

if __name__ == '__main__':
    test_input_id_mapping()