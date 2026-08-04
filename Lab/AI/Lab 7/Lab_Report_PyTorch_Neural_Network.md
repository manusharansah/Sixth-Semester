# Lab Report: Introduction to PyTorch & Custom Neural Networks

**Name:** Manu Sharan Kumar
**Roll No:** ACE080BCT037

---

## Objective

To get hands-on experience with PyTorch's core components — tensors, automatic differentiation, and the `torch.nn` module — and to build, train, and save a custom multilayer neural network.

## What We Did

1. **Explored PyTorch basics**
   - Verified the installed PyTorch version and checked CUDA (GPU) availability.
   - Learned that PyTorch's three core components are the **tensor library**, the **automatic differentiation engine (autograd)**, and the **deep learning utilities** built on top of them.

2. **Worked with tensors**
   - Created scalars, vectors, matrices, and higher-dimensional tensors from Python lists and NumPy arrays.
   - Compared `torch.tensor()` (copies data) with `torch.from_numpy()` (shares memory), observing how changes to the NumPy array did/didn't propagate.
   - Practiced common tensor operations: checking `.dtype` and `.shape`, converting between int and float types, reshaping with `.view()` and `.reshape()`, transposing with `.T`, and matrix multiplication using `.matmul()` and the `@` operator.

3. **Understood computation graphs and autograd**
   - Built a simple logistic regression unit (`x1, w1, b → sigmoid → binary cross-entropy loss`) and computed its loss.
   - Used `requires_grad=True` to track gradients, then computed gradients two ways: manually with `torch.autograd.grad()` and automatically with `loss.backward()`, confirming both gave the same result.

4. **Implemented a custom neural network**
   - Defined a `NeuralNetwork` class inheriting from `torch.nn.Module`, using `torch.nn.Sequential` to stack `Linear` and `ReLU` layers into hidden layers and an output layer (no activation on the output, since raw logits are needed).
   - Inspected the model architecture with `print(model)` and counted trainable parameters using `sum(p.numel() for p in model.parameters() if p.requires_grad)`.
   - Verified the parameter-count formula for each linear layer:
     $$\text{Total Parameters} = (\text{in\_features} \times \text{out\_features}) + \text{out\_features}$$
   - Observed that weights are initialized from a uniform distribution $\mathcal{U}(-\sqrt{k}, \sqrt{k})$ where $k = 1/\text{in\_features}$, and that `torch.manual_seed()` makes this initialization reproducible.
   - Ran a forward pass on random input, then wrapped inference in `torch.no_grad()` to avoid building an unnecessary computation graph, and used `torch.softmax()` to convert logits into class probabilities.

5. **Built a data pipeline**
   - Created a small toy classification dataset (`X_train`, `y_train`, `X_test`, `y_test`).
   - Implemented a custom `Dataset` subclass (`ToyDataset`) with `__getitem__` and `__len__`.
   - Wrapped it in a `DataLoader` to handle batching, shuffling, and (optionally) dropping the last incomplete batch (`drop_last=True`).

6. **Trained the model**
   - Wrote a standard PyTorch training loop over 3 epochs:
     - `model.train()` → forward pass → compute loss with `F.cross_entropy` → `optimizer.zero_grad()` → `loss.backward()` → `optimizer.step()`.
   - Used Stochastic Gradient Descent (`torch.optim.SGD`) as the optimizer and watched the loss drop toward 0 across epochs.

7. **Evaluated the model**
   - Ran inference in `eval()` mode, converted logits to class predictions with `torch.argmax()`, and wrote a `compute_accuracy()` function to measure performance on both the train and test sets (achieved 100% accuracy on this toy dataset).

8. **Saved and loaded the model**
   - Saved the trained parameters with `torch.save(model.state_dict(), "model.pth")`.
   - Reloaded them into a freshly instantiated model of the same architecture using `model.load_state_dict(torch.load(...))`.

## Key Learnings

- PyTorch tensors behave like NumPy arrays but additionally support GPU acceleration and automatic differentiation.
- `torch.nn.Module` and `torch.nn.Sequential` provide a clean, reusable way to define network architectures.
- Autograd automatically tracks operations on tensors with `requires_grad=True`, enabling gradient computation via `.backward()` without manually deriving derivatives.
- A full training loop follows a consistent pattern: **forward pass → compute loss → zero gradients → backward pass → optimizer step**.
- `DataLoader` and `Dataset` simplify batching and shuffling data for training.
- Using `torch.no_grad()` during inference saves memory and computation since gradients aren't needed.
- Model weights can be persisted and restored using `state_dict()`, provided the model architecture is reconstructed identically before loading.

## Conclusion

This lab gave a practical, end-to-end introduction to PyTorch: from tensor manipulation and autograd fundamentals to designing, training, evaluating, and saving a custom feedforward neural network. It reinforced the standard deep learning workflow used across most PyTorch-based projects.
