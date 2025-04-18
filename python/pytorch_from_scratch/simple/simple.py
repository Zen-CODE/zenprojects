"""
Module housing very simple neural network for prediciting the value of a column
"""

import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from torch import nn

BATCH_SIZE = 4

def create_csv(file_name, num_rows=1000, num_cols=10):
    """Create a csv file with the given number of rows and columns filled with
    random integers. The last column is the target and the sum of all previous
    columns."""
    data = pd.DataFrame(
        {f"col_{i}": [torch.randint(0, 10, (1,)).item() for _ in range(num_rows)]
         for i in range(num_cols)}
    )
    data["target"] = data.sum(axis=1)
    data.to_csv(file_name, index=False)


class CSVDataset(Dataset):
    def __init__(self, csv_file, transform=None, target_column='target'):
        """
        Args:
            csv_file (string): Path to the CSV file.
            transform (callable, optional): Optional transform to be applied
                on a sample.
            target_column (string): Name of the column containing the target variable.
        """
        self.data = pd.read_csv(csv_file)
        self.transform = transform
        self.target_column = target_column
        self.feature_columns = [col for col in self.data.columns if col != self.target_column]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = self.data.loc[idx, self.feature_columns].values
        target = self.data.loc[idx, self.target_column]

        features = torch.tensor(features, dtype=torch.float32)
        target = torch.tensor(target, dtype=torch.float32)  # Or torch.long for classification

        if self.transform:
            features = self.transform(features)

        return features, target


class CSVDataset(Dataset):
    def __init__(self, csv_file, target_col=-1, transform=None):
        self.data = pd.read_csv(csv_file)
        self.target_col = target_col  # Column index for the target
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        target = torch.tensor(row[self.target_col], dtype=torch.float32) #or torch.long for classification
        features = row.drop(self.data.columns[self.target_col]) #Drop the target column.
        features_numeric = []

        for val in features:
            if isinstance(val, (int, float, torch.Tensor)): #check if numeric
                features_numeric.append(float(val))
            elif isinstance(val, str):
                # Handle strings (e.g., one-hot encoding, integer encoding)
                # This example will replace strings with 0.0, but you will want to change this.
                # features_numeric.append(0.0) #placeholder.
                features_numeric.append(torch.ByteTensor(
                    list(bytes(val, 'utf8'))))
            else:
                # features_numeric.append(0.0) #Default to 0.0 for unknown data.
                print("Warning: item skepped - ", val)

        features_tensor = torch.tensor(features_numeric, dtype=torch.float32)

        if self.transform:
            features_tensor = self.transform(features_tensor)

        return features_tensor, target


class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(10, 1),
            nn.ReLU(),
            nn.Linear(10, 1),
            nn.ReLU(),
            nn.Linear(10, 1)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    @staticmethod
    def get_model():
        """Return an instance of the Neural Network model."""

class LinearRegression(nn.Module):
    def __init__(self, input_size, output_size):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x):
        return self.linear(x)


def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


if __name__ == "__main__":
    # # For generating the CSV files.
    # create_csv('./simple/simple_train.csv', num_rows=1000)
    # create_csv('./simple/simple_test.csv', num_rows=100)

    # Get datasets
    train_dataset = CSVDataset(csv_file='./simple/simple_train.csv')
    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE,
                                  shuffle=True)
    test_dataset = CSVDataset(csv_file='./simple/simple_test.csv')
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

    # Get model
    device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
    print(f"Using {device} device")
    model = NeuralNetwork().to(device)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

    epochs = 5
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train(train_dataloader, model, loss_fn, optimizer)
        test(test_dataloader, model, loss_fn)
    print("Done!")