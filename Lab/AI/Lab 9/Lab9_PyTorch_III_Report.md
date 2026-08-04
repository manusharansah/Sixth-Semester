# Lab 9 Report: Introduction to PyTorch III — GPU Training and Custom CNNs

## Objective

This lab explored how PyTorch handles computation across CPU and GPU devices, and how to build a custom Convolutional Neural Network (CNN) using `nn.Module`. It builds on the PyTorch fundamentals from earlier appendix material and extends them with GPU performance comparisons and a real image-classification model on MNIST.

## Part 1: PyTorch Fundamentals on GPU Devices

We started with the basics of moving tensors between devices:

- Checked PyTorch version and GPU availability with `torch.__version__` and `torch.cuda.is_available()`.
- Verified that tensors located on **different devices cannot be combined directly** — adding a CPU tensor and a GPU tensor raises a `RuntimeError`. All operands must be moved to the same device with `.to(device)` first.
- Built a small feedforward `NeuralNetwork` (two hidden layers) and trained it on a toy 2D classification dataset using a `Dataset`/`DataLoader` pipeline, moving both the model and each batch to the target device with `.to(device)`.
- Wrote a `compute_accuracy()` helper that also respects device placement, and confirmed 100% accuracy on the toy train/test sets.

**Key lesson:** in PyTorch, the model and all its input tensors must live on the same device, and this has to be done explicitly — nothing happens automatically.

## Part 2: GPU vs. CPU — Training and Inference Timing

Using a larger feedforward network (2 hidden layers of 500 units, 1000-dim dummy input) so device differences would actually be measurable, we compared CPU and GPU performance:

| Metric | CPU | GPU | Speedup |
|---|---|---|---|
| Training (5 epochs) | 1.61 s | 0.84 s | ~1.91× |
| Inference (50 forward passes) | 0.699 s | 0.036 s | ~19.65× |

**What we learned:**
- GPUs accelerate both training and inference because matrix multiplications and convolutions parallelize well across the GPU's many cores, while CPUs execute mostly sequentially.
- The GPU speedup is much larger for inference than training in this case, since inference has no backward pass or optimizer step to bottleneck things.
- `torch.cuda.synchronize()` must be called before stopping a timer on GPU operations, because CUDA calls are launched **asynchronously** — without it, timing would be misleadingly fast.
- For very small/toy models, GPU can actually be *slower* than CPU due to the fixed overhead of transferring data to the device — the speedup only shows up once the model/data is large enough.
- The output tensor's device always matches wherever the model and inputs were placed. A GPU tensor cannot be converted directly with `.numpy()` (it raises a `TypeError`); it must be moved back with `.cpu()` first, e.g. `output.cpu().numpy()`.

## Part 3: Building a Custom CNN (`nn.Module`) for MNIST

The second task translated a whiteboard notation into a working CNN.

### Interpreting `Conv2d(1, 6, 5, 1)`
The four numbers map to `nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5, stride=1)`: a single grayscale input channel, 6 learned filters (each producing its own feature map), a 5×5 sliding kernel, moving 1 pixel at a time.

### Output size formula
$$\text{Output Size} = \frac{W-K}{S} + 1$$

Applying this to a 32×32 input with a 5×5 kernel and stride 1 gives `(32-5)/1 + 1 = 28`, shrinking the spatial size to 28×28 while the channel count grows to `out_channels`. Since MNIST images are natively 28×28, we padded them to 32×32 with `transforms.Pad(2)` to reproduce this exact classic **LeNet-5** sizing.

### Architecture (LeNet-5 style)
Traced step by step and then implemented as a `CustomCNN(nn.Module)`:

1. `Conv2d(1, 6, 5, 1)` → 32×32 → 28×28
2. `MaxPool2d(2, 2)` → 28×28 → 14×14
3. `Conv2d(6, 16, 5, 1)` → 14×14 → 10×10
4. `MaxPool2d(2, 2)` → 10×10 → 5×5
5. Flatten → 16×5×5 = 400
6. Fully connected layers: 400 → 120 → 84 → 10 (digit classes)

Pooling layers halve the spatial size without adding any learnable parameters — they just downsample.

### Training
- Data: MNIST, split into 50,000 train / 10,000 validation / 10,000 test images, loaded via `DataLoader`.
- Loss: `CrossEntropyLoss` (standard for multi-class classification).
- Optimizer: `Adam` (lr = 0.001), chosen over plain SGD for faster convergence on CNNs.
- Trained for 5 epochs, tracking training/validation loss and accuracy per epoch, with the same `model.train()` / `model.eval()` + `torch.no_grad()` pattern used in Part 2.

### Results
- **Test accuracy: 9876/10000 = 98.76%**
- A single test image was run through the trained model in `eval()` mode; the predicted digit matched the true label, and the output tensor's device (`cpu`) was confirmed with `.device`, tying directly back to the device-placement lesson from Part 1/2.

## Overall Takeaways

1. **Device management is manual and explicit** in PyTorch — the model, inputs, and any conversions (e.g., to NumPy) all need `.to(device)` / `.cpu()` calls to line up.
2. **GPUs give the largest speedups on larger, matrix-heavy workloads**; tiny toy examples may not benefit due to transfer overhead, and GPU timers need `torch.cuda.synchronize()` to be accurate.
3. **`nn.Conv2d` parameters and the `(W-K)/S + 1` output-size formula** describe exactly how convolutions transform spatial dimensions, and this reasoning scales up directly into a full CNN architecture (LeNet-5) that achieves ~98.8% accuracy on MNIST.
4. The lab connected low-level tensor/device mechanics (Part 1–2) to a complete, practical deep learning pipeline (Part 3): data loading → model definition → training loop → evaluation → single-sample inference.
