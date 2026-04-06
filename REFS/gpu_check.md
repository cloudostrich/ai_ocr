# GPU Support for llama-cpp-python

## Quick Check: `llama_check.py`

Run this script to verify if your `llama-cpp-python` installation supports GPU offloading:

```bash
uv run python llama_check.py
```

**Expected output (GPU supported):**
```
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4070 Laptop GPU, compute capability 8.9, VMM: yes
Supports GPU offload: True
```

If you see `Supports GPU offload: False`, you need to reinstall `llama-cpp-python` with CUDA support.

---

## Offloading Layers to GPU

When loading a model, use `n_gpu_layers` to control GPU offloading:

```python
from llama_cpp import Llama

llm = Llama(
    model_path="/path/to/your/model.gguf",
    n_gpu_layers=-1,  # -1 = all layers on GPU, 0 = CPU only
    verbose=True      # Shows which layers are offloaded
)
```

| `n_gpu_layers` | Behavior |
|----------------|----------|
| `-1` | Offload all layers to GPU |
| `0` | CPU only (no GPU) |
| `N` | Offload first N layers to GPU |

**Verbose output example:**
```
llm_load_tensors: offloading 32 repeating layers to GPU
llm_load_tensors: offloaded 32/33 layers to GPU
```

---

## Monitoring GPU Usage with nvidia-smi

### Real-time monitoring
```bash
# Update every 1 second
nvidia-smi -l 1

# Or with watch
watch -n 1 nvidia-smi
```

### Compact output (memory & utilization only)
```bash
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv -l 1
```

### What to look for
- **Memory-Usage**: Increases when model loads (e.g., `2048MiB / 8192MiB`)
- **GPU-Util**: Shows activity during inference (e.g., `45%`)
- **Processes**: Your Python process should appear in the process list
