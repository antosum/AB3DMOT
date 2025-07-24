#!/usr/bin/env python3
"""
Example: How to use the new input bbox ID preservation feature in AB3DMOT

This example shows the new API and expected behavior without requiring
the full AB3DMOT environment setup.
"""

def demonstrate_api():
    """Demonstrate the new API usage"""
    
    print("=== AB3DMOT Input Bbox ID Preservation ===\n")
    
    print("1. SETUP - Initialize tracker as before:")
    print("   tracker = AB3DMOT(cfg, cat='Car')")
    print()
    
    print("2. NEW API - Track with input bbox IDs:")
    print("   # Your input bboxes with original IDs")
    print("   input_bboxes = [bbox1, bbox2, bbox3]")
    print("   input_ids = [100, 200, 300]  # Your original bbox identifiers")
    print()
    print("   # Track with ID preservation (NEW PARAMETER)")
    print("   results, affi, id_mapping = tracker.track(")
    print("       {'dets': input_bboxes, 'info': info},")
    print("       frame=5,")
    print("       seq_name='seq01',")
    print("       input_ids=input_ids  # <-- NEW PARAMETER")
    print("   )")
    print()
    
    print("3. RESULTS - What you get back:")
    print("   results: Same as before - tracked objects with AB3DMOT track IDs")
    print("   affi: Same as before - affinity matrix")
    print("   id_mapping: NEW - Dictionary mapping track IDs to your input IDs")
    print()
    
    print("4. EXAMPLE OUTPUT:")
    print("   Input: 3 bboxes with IDs [100, 200, 300]")
    print("   Output: 2 tracks with AB3DMOT IDs [501, 502] (filtered by min_hits, etc.)")
    print("   id_mapping = {501: 200, 502: 100}")
    print("   Meaning:")
    print("     - Track 501 corresponds to your input bbox 200")
    print("     - Track 502 corresponds to your input bbox 100") 
    print("     - Your input bbox 300 was filtered out")
    print()
    
    print("5. EDGE CASES:")
    print("   id_mapping = {501: 200, 502: None, 503: 100}")
    print("   Meaning:")
    print("     - Track 501: came from your input bbox 200")
    print("     - Track 502: propagated from previous frame (no current detection)")
    print("     - Track 503: came from your input bbox 100")
    print()
    
    print("6. BACKWARD COMPATIBILITY:")
    print("   # Old API still works exactly the same")
    print("   results, affi = tracker.track(dets_all, frame, seq_name)")
    print("   # New API is optional - only use input_ids if you need ID mapping")
    print()
    
    print("=== Key Benefits ===")
    print("✓ Complete traceability: Know which output track came from which input bbox")
    print("✓ Handle filtered objects: Understand why some inputs don't produce outputs")
    print("✓ Track propagation: Distinguish between current detections vs. predicted tracks")
    print("✓ Backward compatible: Existing code works unchanged")
    print("✓ Minimal overhead: Only adds ID fields and mapping logic")
    
    print("\n=== Implementation Complete ===")
    print("The AB3DMOT tracker now supports input bbox ID preservation!")

if __name__ == '__main__':
    demonstrate_api()