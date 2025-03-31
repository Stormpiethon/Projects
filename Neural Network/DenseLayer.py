from BaseLayer import Layer
import numpy as np

# Class to represent the dense layer of the Neural Network 
class Dense(Layer):
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(output_size, input_size)
        self.bias = np.random.randn(output_size, 1)

    # Forward propogation method for data traveling from input to output in the neural network
    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.bias

    # Backward propogation method that is used to adjust the weights and bias of the neural network
    def backward(self, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, self.input.T)
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * output_gradient
        return np.dot(self.weights.T, output_gradient)