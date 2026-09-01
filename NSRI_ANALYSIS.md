# NSRI Implementation Analysis

## Current Formulas (Already Implemented)

### 1. SAI (Stress Accumulation Index)
**Location:** `services/nsri_service.py` - `calculate_sai()`

```python
SAI = (sum of available stress probabilities) / (number of probabilities) * 100
```

**Details:**
- Takes 0-2 optional stress probabilities (wesad_stress_probability, mmash_stress_probability)
- Averages the available probabilities
- Converts to 0-100 scale
- Returns None if no probabilities provided
- Rounded to 2 decimal places

**Example:**
- SAI(0.7, 0.5) = (0.7 + 0.5) / 2 * 100 = 60.0
- SAI(0.85, None) = 0.85 * 100 = 85.0

### 2. PRI (Physiological Recovery Index)
**Location:** `services/nsri_service.py` - `calculate_pri()`

```python
PRI = 0.6 * hrv_normalized + 0.4 * (1 - resting_hr_normalized) * 100
```

**Details:**
- Requires BOTH hrv_normalized AND resting_hr_normalized (both 0-1 normalized values)
- Returns None if either input is missing
- HRV component: 60% weight (higher is better recovery)
- Resting HR component: 40% weight (lower is better recovery, hence the inversion)
- Converts to 0-100 scale
- Rounded to 2 decimal places

**Example:**
- PRI(0.8, 0.3) = (0.6 * 0.8 + 0.4 * (1 - 0.3)) * 100 = 76.0
- PRI(0.0, 0.0) = (0.6 * 0.0 + 0.4 * 1.0) * 100 = 40.0

---

## Missing Components

### 3. RDT (Recovery During Training) - ❌ NOT DEFINED
**Location:** Not found anywhere in the codebase

**What we know:**
- Not implemented
- Not mentioned in any code comments
- Not mentioned in test files
- Not mentioned in notebooks
- Not mentioned in any documentation

**What's missing:**
1. No formula definition
2. No input specification (what data is needed?)
3. No calculation logic
4. No tests or examples

### 4. Final NSRI - ❌ NOT DEFINED
**Location:** Not found anywhere in the codebase

**What we know:**
- Not implemented
- Current `/api/v1/nsri/calculate` only returns `{sai: value, pri: value}`
- No final aggregation or combination logic exists
- Not mentioned in tests, documentation, or comments

**What's missing:**
1. No formula definition (how does final NSRI combine SAI, PRI, and RDT?)
2. No endpoint parameter or calculation logic
3. No test cases

---

## Available Inputs in API

### Current `/api/v1/nsri/calculate` Request Schema
```python
class NSRIRequest(BaseModel):
    wesad_stress_probability: Optional[float] = None      # 0-1
    mmash_stress_probability: Optional[float] = None      # 0-1
    hrv_normalized: Optional[float] = None                # 0-1
    resting_hr_normalized: Optional[float] = None         # 0-1
    user_id: Optional[str] = None                         # For DB saving
    measurement_id: Optional[str] = None                  # For DB saving
```

### Missing Inputs for RDT
Since RDT is not defined, we don't know what inputs it needs. Possible candidates (speculation only):
- Training duration/intensity
- Recovery time duration
- Heart rate variability during recovery
- Sleep data
- Stress level changes over time
- Muscle tension measurements
- Any training-specific metrics

**⚠️ Cannot determine without the RDT formula definition**

---

## Database Structure

### Collections that exist:
```python
predictions_collection    # Stores model predictions
nsri_collection          # Stores NSRI results
```

### Current NSRI result structure saved:
```python
{
    "user_id": str,
    "measurement_id": str,
    "created_at": datetime,
    "data": {
        "sai": float,
        "pri": float
    }
}
```

**Note:** If final NSRI is implemented, the "data" field structure will need to be updated to include the final NSRI value.

---

## Summary Table

| Component | Status | Formula | Inputs | Database | Tests |
|-----------|--------|---------|--------|----------|-------|
| SAI | ✅ Done | Defined | ✅ Clear | ✅ Saving | ✅ 7 tests |
| PRI | ✅ Done | Defined | ✅ Clear | ✅ Saving | ✅ 8 tests |
| RDT | ❌ Missing | NOT DEFINED | ❓ Unknown | ❌ No | ❌ No |
| Final NSRI | ❌ Missing | NOT DEFINED | ❌ Unknown | ❌ No | ❌ No |

---

## What Would Be Needed to Implement RDT and Final NSRI

### Step 1: Define RDT Formula
**Required Information:**
- What is RDT mathematically?
- What inputs does it need?
- What is its output range (0-1, 0-100)?
- How should it handle missing data?

### Step 2: Update API Schema
**Add to `NSRIRequest`:**
- All new fields required for RDT calculation
- Example: training_duration, recovery_time, training_intensity, etc.

### Step 3: Implement RDT Calculation
**In `services/nsri_service.py`:**
- Add `calculate_rdt()` method to NSRIService class
- Handle optional/missing inputs
- Return None if insufficient data

### Step 4: Define Final NSRI Formula
**Required Information:**
- Is it a weighted combination of SAI + PRI + RDT?
- What are the weights?
- How does it handle missing components?
- What is the output range?

### Step 5: Update NSRI Route
**In `routes/nsri.py`:**
- Call new `calculate_rdt()` method
- Call new final NSRI calculation method
- Update response to include rdt and final NSRI
- Update database structure if needed

### Step 6: Update Database
**Possible changes:**
- Update `nsri_collection` structure to store RDT and final NSRI
- May need schema migration for existing records

### Step 7: Add Tests
**Add test cases for:**
- RDT calculation with various inputs
- Final NSRI calculation
- Edge cases and missing data handling
- Boundary conditions

---

## Current API Response

### Current `/api/v1/nsri/calculate` Response:
```json
{
    "sai": 60.0,
    "pri": 76.0
}
```

### Expected Future Response (example):
```json
{
    "sai": 60.0,
    "pri": 76.0,
    "rdt": ???,  // Cannot determine without formula
    "nsri": ???  // Cannot determine without formula
}
```

---

## Next Steps (Recommendation)

**BLOCKED:** Cannot implement RDT or Final NSRI without:
1. ✅ RDT formula definition (mathematical definition)
2. ✅ Final NSRI formula definition (how it combines SAI, PRI, RDT)
3. ✅ Clear specification of inputs needed for RDT
4. ✅ Expected output ranges and precision

**ACTION REQUIRED:** User must provide:
- The mathematical formula for RDT
- The mathematical formula for Final NSRI
- Input requirements for RDT calculation
- Any relevant research papers or documentation
