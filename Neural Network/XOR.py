# Combining all of the different Neural Network code
from DenseLayer import Dense
from HyperbolicTangent import Tanh
from MeanSquaredError import mse, mse_prime
import numpy as np

X = np.reshape([[0, 0], [0, 1], [1, 0], [1, 1]], (4, 2, 1))
Y = np.reshape([[0], [1], [1], [0]], (4, 1, 1))

# Shape of the network is 2 nodes in the input layer going to 3 nodes in the next, then from 3
# nodes to 1 node in the output layer.
network = [
    Dense(2, 3),
    Tanh(),
    Dense(3, 1),
    Tanh()
]

epochs = 10000
learning_rate = 0.1

# Training the model
for e in range(epochs):
    error = 0
    for x, y in zip(X, Y):
        # Forward propogation
        output = x
        for layer in network:
            output = layer.forward(output)

        # Error doesn't need to be calculated here, it is just done so that it can be displayed
        error += mse(y, output)

        # Back propogation
        grad = mse_prime(y, output)
        for layer in reversed(network):
            grad = layer.backward(grad, learning_rate)

    error /= len(X)
    print('%d/%d, error=%f' % (e + 1, epochs, error))