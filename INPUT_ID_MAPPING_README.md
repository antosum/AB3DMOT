# AB3DMOT Input Bbox ID Preservation

## Overview
This enhancement adds the ability to preserve input bounding box IDs through the AB3DMOT tracking pipeline, allowing you to match output tracklets with your original input bounding boxes.

## Problem Solved
- **Before**: AB3DMOT would output fewer objects than input (due to filtering) in a different order, with no way to know which output track corresponded to which input bbox
- **After**: Complete traceability from input bbox IDs to output track IDs

## New API

### Method Signature
```python
results, affi, id_mapping = tracker.track(dets_all, frame, seq_name, input_ids=None)
```

### New Parameters
- `input_ids` (optional): List of original bbox IDs corresponding to each detection

### New Return Value
- `id_mapping`: Dictionary mapping `{track_id: input_id}` or `{track_id: None}` for propagated tracks

## Usage Example

```python
# Your input bboxes with original IDs
input_bboxes = [bbox1, bbox2, bbox3]
input_ids = [100, 200, 300]

# Track with ID preservation
results, affi, id_mapping = tracker.track(
    {'dets': input_bboxes, 'info': info}, 
    frame=5, 
    seq_name='seq01',
    input_ids=input_ids
)

# Interpret results
# id_mapping = {501: 200, 502: None, 503: 100}
# - Track 501 came from your input bbox 200
# - Track 502 is propagated from previous frame (no current detection)  
# - Track 503 came from your input bbox 100
```

## Implementation Details

### Files Modified
1. **`AB3DMOT_libs/box.py`**: Added `input_id` field to `Box3D` class
2. **`AB3DMOT_libs/kalman_filter.py`**: Added `input_id` field to `KF` class
3. **`AB3DMOT_libs/model.py`**: 
   - Added `input_ids` parameter to `track()` method
   - Updated `process_dets()` to propagate input IDs
   - Added ID mapping logic using matching results
   - Extended return format

### Key Algorithm Components

#### 1. ID Propagation
- Input IDs stored in `Box3D` objects during `process_dets()`
- Propagated to `KF` trackers during birth process
- Preserved through track lifecycle

#### 2. ID Mapping Logic
Uses the existing `matched` array from data association:
```python
# Map matched detections: input_id → detection_index → track_id
for match in matched:
    det_idx, trk_idx = match[0], match[1]
    track_id = self.trackers[trk_idx].id
    input_id = dets[det_idx].input_id
    id_mapping[track_id] = input_id

# Map new births: input_id → unmatched_detection → new_track_id  
for i, unmatched_det_idx in enumerate(unmatched_dets):
    new_track_id = new_id_list[i]
    input_id = dets[unmatched_det_idx].input_id
    id_mapping[new_track_id] = input_id

# Map unmatched tracks (propagated without detection)
for trk_idx in unmatched_trks:
    track_id = self.trackers[trk_idx].id
    id_mapping[track_id] = None
```

## Backward Compatibility
- **Fully backward compatible**: Existing code works unchanged
- `input_ids` parameter is optional
- When not provided, behavior is identical to original AB3DMOT

## Benefits
- ✅ **Complete traceability**: Know which output track came from which input bbox
- ✅ **Handle filtering**: Understand why some inputs don't produce outputs  
- ✅ **Track propagation**: Distinguish current detections vs. predicted tracks
- ✅ **Minimal overhead**: Only adds ID fields and mapping logic
- ✅ **Production ready**: Safe for existing codebases

## Testing
- Run `python input_id_mapping_example.py` to see API demonstration
- Integration testing requires full AB3DMOT environment with Xinshuo_PyToolbox

## Use Cases
- **Multi-sensor fusion**: Track correspondence across sensor modalities
- **Pipeline integration**: Connect detection and tracking stages  
- **Evaluation metrics**: Compute detection-to-track correspondence statistics
- **Debugging**: Understand which detections become successful tracks
- **Data analysis**: Study detection filtering and track lifecycle patterns