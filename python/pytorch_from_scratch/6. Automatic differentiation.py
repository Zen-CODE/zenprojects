# Automatic Differentiation with torch.autograd

# When training neural networks, the most frequently used algorithm is back
# propagation. In this algorithm, parameters (model weights) are adjusted
# according to the gradient of the loss function with respect to the given
# parameter.

# Consider the simplest one-layer neural network, with input x, parameters w
# and b, and some loss function.

import torch

x = torch.ones(5)  # input tensor
y = torch.zeros(3)  # expected output
w = torch.randn(5, 3, requires_grad=True)
b = torch.randn(3, requires_grad=True)
z = torch.matmul(x, w)+b
loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y)

print(f"Gradient function for z = {z.grad_fn}")
print(f"Gradient function for loss = {loss.grad_fn}")

# To optimize weights of parameters in the neural network, we need to compute
# the derivatives of our loss function with respect to parameters.

loss.backward()
print(w.grad)
print(b.grad)

# By default, all tensors with requires_grad=True are tracking their
# computational history and support gradient computation.
# However, there are some cases when we do not need to do that,
# for example, when we have trained the model and just want to apply it to some
# input data.

z = torch.matmul(x, w)+b
print(z.requires_grad)

with torch.no_grad():
    z = torch.matmul(x, w)+b
print(z.requires_grad)

# Another way to achieve the same result is to use the detach() method:

z = torch.matmul(x, w)+b
z_det = z.detach()
print(z_det.requires_grad)
