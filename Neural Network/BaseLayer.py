# Base class that all the different layers of the Neural Network can inherit from, basically abstract
class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # These functions are overridden in the other layers
    def forward(self, input):
        # TODO: return output
        pass

    def backward(self, output_gradient, learning_rate):
        # TODO: update parameters and return input_gradient
        pass


