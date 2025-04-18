import torch
import numpy as np

# From data
data = [[1, 2],[3, 4]]
x_data = torch.tensor(data)

# From Numpy array
np_array = np.array(data)
x_np = torch.from_numpy(np_array)

# From another tensor
x_ones = torch.ones_like(x_data) # retains the properties of x_data
print(f"Ones Tensor: \n {x_ones} \n")
x_rand = torch.rand_like(x_data, dtype=torch.float) # overrides the datatype
print(f"Random Tensor: \n {x_rand} \n")


# With random or constant values: shape is a tuple of tensor dimensions.
# In the functions below, it determines the dimensionality of the output tensor.
shape = (2,3,)
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape)
zeros_tensor = torch.zeros(shape)

print(f"Random Tensor: \n {rand_tensor} \n")
print(f"Ones Tensor: \n {ones_tensor} \n")
print(f"Zeros Tensor: \n {zeros_tensor}")

# === Attributes of a Tensor
# Tensor attributes describe their shape, datatype, and the device on which
# they are stored.

tensor = torch.rand(3,4)

print(f"Shape of tensor: {tensor.shape}")
print(f"Datatype of tensor: {tensor.dtype}")
print(f"Device tensor is stored on: {tensor.device}")

# Index operations
tensor = torch.ones(4, 4)
print(f"First row: {tensor[0]}")
print(f"First column: {tensor[:, 0]}")
print(f"Last column: {tensor[..., -1]}")
tensor[:,1] = 0
print(tensor)

t1 = torch.cat([tensor, tensor, tensor], dim=1)
print(t1)

# Arithmetic operations

# This computes the matrix multiplication between two tensors. y1, y2, y3 will have the same value
# ``tensor.T`` returns the transpose of a tensor
y1 = tensor @ tensor.T
y2 = tensor.matmul(tensor.T)
y3 = torch.rand_like(y1)
torch.matmul(tensor, tensor.T, out=y3)

# This computes the element-wise product. z1, z2, z3 will have the same value
z1 = tensor * tensor
z2 = tensor.mul(tensor)

z3 = torch.rand_like(tensor)
torch.mul(tensor, tensor, out=z3)

# In-place operations Operations that store the result into the operand are called in-place.
# They are denoted by a _ suffix. For example: x.copy_(y), x.t_(), will change x.

print(f"{tensor} \n")
tensor.add_(5)
print(tensor)

## Bridge with NumPy

# Tensor to NumPy array
t = torch.ones(5)
print(f"t: {t}")
n = t.numpy()
print(f"n: {n}")

# There is a lot more you can do. For more, please see
# https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html
