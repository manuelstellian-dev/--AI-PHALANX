# 🏛️ Λ-MÖBIUS ENGINE - Quick Start Guide

**ΜΟΛΩΝ ΛΑΒΕ!** - Get started with temporal compression in 5 minutes.

---

## 🚀 Quick Start

### 1. Basic Usage

```python
from control.kronos_arbiter import KronosArbiter

# Initialize Kronos with built-in Λ-MÖBIUS Engine
kronos = KronosArbiter(n_cores=4)

# Calculate supreme time metrics
metrics = kronos.calculate_supreme_time(
    k=100,    # Compression constant
    P=4,      # Parallelism factor (cores)
    U=10      # Universe size (workload)
)

# Access results
print(f"T_supreme: {metrics.T_supreme:.3f}s")
print(f"State: {metrics.state.name}")
```

### 2. Get Current State

```python
# Get the current Lambda state
state = kronos.get_lambda_state()

# State can be:
# - LambdaState.WRAP (+1): Compression mode
# - LambdaState.STEADY (0): Balanced operation
# - LambdaState.UNWRAP (-1): Diagnostic mode

print(f"Current state: {state.name} ({state.value})")
```

### 3. Access All Metrics

```python
# Full metrics object
print(f"T_wrap: {metrics.T_wrap:.3f}s")        # Compression time
print(f"T_mult: {metrics.T_mult:.3f}s")        # Distribution time
print(f"T_hybrid: {metrics.T_hybrid:.3f}s")    # Harmonic mean
print(f"T_balance: {metrics.T_balance:.3f}s")  # Geometric mean
print(f"T_supreme: {metrics.T_supreme:.3f}s")  # Selected optimal
```

### 4. View History

```python
# Get last 10 calculations
history = kronos.lambda_mobius.get_history(last_n=10)

for entry in history:
    print(f"U={entry['U']}: T_supreme={entry['T_supreme']:.3f}s")
```

---

## 🌐 API Endpoint

### Endpoint Details

- **URL:** `/api/v1/lambda-mobius`
- **Method:** GET
- **Authentication:** Required (Bearer token)

### cURL Example

```bash
curl -X GET "http://localhost:7300/api/v1/lambda-mobius" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Response Format

```json
{
  "current_metrics": {
    "T_wrap": 1.001,
    "T_mult": 2.308,
    "T_hybrid": 0.698,
    "T_balance": 1.520,
    "T_supreme": 1.001,
    "state": "WRAP",
    "state_value": 1,
    "k": 100,
    "P": 4,
    "U": 10,
    "timestamp": 1730589845.123
  },
  "current_state": "WRAP",
  "state_value": 1,
  "history": [
    {
      "T_wrap": 1.001,
      "T_mult": 2.308,
      "T_supreme": 1.001,
      "state": "WRAP",
      "U": 10,
      "timestamp": 1730589845.123
    }
  ],
  "timestamp": 1730589845.123
}
```

---

## 📊 Understanding States

### WRAP State (+1)

**When:** `k * P * (1 + ln U) > 100`

**Use Case:** High-performance mode with aggressive optimization

**Example:**
```python
metrics = kronos.calculate_supreme_time(k=100, P=10, U=10)
# k * P * (1 + ln 10) = 100 * 10 * 3.303 = 3303 > 100
# Result: WRAP state, uses T_wrap for T_supreme
```

### STEADY State (0)

**When:** Neither WRAP nor UNWRAP conditions met

**Use Case:** Normal balanced operation

**Example:**
```python
metrics = kronos.calculate_supreme_time(k=1, P=1, U=10)
# k * P * (1 + ln 10) = 1 * 1 * 3.303 = 3.303 < 100
# U = 10 < 1000
# Result: STEADY state, uses T_hybrid for T_supreme
```

### UNWRAP State (-1)

**When:** `U > 1000`

**Use Case:** Large workloads requiring detailed analysis

**Example:**
```python
metrics = kronos.calculate_supreme_time(k=1, P=1, U=2000)
# U = 2000 > 1000
# Result: UNWRAP state, uses T_mult for T_supreme
```

---

## 🔧 FFP Pipeline Integration

The Fractal Flux Pipeline uses Λ-MÖBIUS for adaptive timing:

```python
from control.fractal_pipeline import FractalFluxPipeline

# Initialize FFP with brain
ffp = FractalFluxPipeline(leonidas_brain)

# Start autoreparatory loop
await ffp.run_forever()

# FFP automatically adjusts cycle timing using:
# T_supreme from Λ-MÖBIUS Engine
```

---

## 📈 Performance Tips

1. **For Speed:** Use higher k and P values to trigger WRAP state
2. **For Accuracy:** Increase U to trigger UNWRAP state
3. **For Balance:** Let Λ-Arbiter choose automatically
4. **For Monitoring:** Check history periodically for trends

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all lambda_mobius tests
pytest tests/test_lambda_mobius.py -v

# Check coverage
pytest tests/test_lambda_mobius.py --cov=control.lambda_mobius

# Run all tests
pytest tests/ -v
```

---

## 📚 Additional Resources

- **Full Documentation:** `docs/LAMBDA_MOBIUS.md`
- **Architecture:** `ARCHITECTURE.md`
- **Temporal Compression Plan:** `TEMPORAL_COMPRESSION_MASTER_PLAN.md`
- **Source Code:** `control/lambda_mobius.py`
- **Tests:** `tests/test_lambda_mobius.py`

---

**ΜΟΛΩΝ ΛΑΒΕ!** 🏛️⚡🔥
