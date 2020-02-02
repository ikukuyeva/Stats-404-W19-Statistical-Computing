"""
network.py
~~~~~~~~~~
Author: Michael Nielsen
Modified by: Irina Kukuyeva
Book: http://neuralnetworksanddeeplearning.com/
Code repository:
https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/src/network.py

A module to implement gradient descent learning algorithm for a feedforward
neural network.  Gradients are calculated using backpropagation.  Note that
I have focused on making the code simple, easily readable, and easily
modifiable.  It is not optimized, and omits many desirable features.
"""

# Standard library
import random

# Third-party libraries
import numpy as np


# Helper functions not part of Network() class, but are used within class:
def sigmoid(z):
    """The sigmoid function: prob of each neuron is between 0 and 1,
       vs softmax(), where prob of output is b/w 0 and 1.
    """
    return 1.0/(1.0 + np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z) * (1 - sigmoid(z))


class Network():
    """Neural network implemented in base Python, which is easier to debug and
       understand what's going on.
    """
    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
           respective layers of the network.  For example, if the list
           was [2, 3, 1] then it would be a three-layer network, with the
           first layer containing 2 neurons, the second layer 3 neurons,
           and the third layer 1 neuron.
           ---
           The biases and weights for the network are initialized randomly,
           using a Gaussian distribution with mean 0, and variance 1.
           - Note that the first layer is assumed to be an input layer, and by
             convention we won't set any biases for those neurons, since biases
             are only ever used in computing the outputs from later layers.
           - Note that there are no weights in the last layer, as it's the
             output layer.
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for bias, wgt in zip(self.biases, self.weights):
            a = sigmoid(np.dot(wgt, a) + bias)
        return a

    def SGD(self, training_data, learning_rate):
        """Train the neural network using gradient descent. ``training_data``
           is a list of tuples ``(x, y)`` representing the training inputs and
           the desired outputs.
        """
        accuracy_new = 0
        while accuracy_new < 0.8:
            accuracy_old = accuracy_new
            nabla_b = [np.zeros(bias.shape) for bias in self.biases]
            nabla_w = [np.zeros(wgt.shape) for wgt in self.weights]
            # --- Iterate over each labeled image in the data set:
            for x, y in training_data:
            	# --- Find small updates to weights and biases that may result
            	#     in better fit:
                delta_nabla_b, delta_nabla_w = self.backprop(x, y)
                nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
                nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            # --- Update weights and biases:
            self.weights = [w - (learning_rate/len(training_data)) * nw
                            for w, nw in zip(self.weights, nabla_w)]
            self.biases = [b - (learning_rate/len(training_data)) * nb
                           for b, nb in zip(self.biases, nabla_b)]
            # --- Evaluate model fit:
            true_positives = self.evaluate(training_data)
            accuracy_new = float(true_positives)/len(training_data)
            print(accuracy_new)
            if abs(accuracy_new - accuracy_old) < 0.00001:
            	# --- Stopping criteria, if model accuracy does not change:
                break
        return self.evaluate(training_data, accuracy=False)

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
           gradient for the cost function C_x.  ``nabla_b`` and
           ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
           to ``self.biases`` and ``self.weights``.
        """
        nabla_b = [np.zeros(bias.shape) for bias in self.biases]
        nabla_w = [np.zeros(wgt.shape) for wgt in self.weights]
        # --- Feedforward (through each layer, starting from the first):
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] 		  # list to store all the z vectors, layer by layer,
        				  #      where z is the "value" of node, before it's
        				  #      passed to activation fcn
        for bias, wgt in zip(self.biases, self.weights):
            z = np.dot(wgt, activation) + bias
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # --- Backward pass (through each layer, starting from the last):
        #
        # Equation BP1 in book:
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        # Equation BP3 in book:
        nabla_b[-1] = delta
        # Equation BP4 in book:
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Here, l = 1 means the last layer of neurons, l = 2 is second-to-last
        # layer, etc., to take advantage of Python's use of negative indices:
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            # Equation BP2 in book:
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            # Equation BP3 in book:
            nabla_b[-l] = delta
            # Equation BP4 in book:
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        # Find small updates to weights and biases that may result in better fit:
        return (nabla_b, nabla_w)

    def evaluate(self, test_data, accuracy=True):
        """Return overall network accuracy or probabilities of each neuron given
           by the network.
		   ---
		   TODO: Candidate for refactoring, as uses if/else statement w/ output.
        """
        # For each labeled image in the data set, see which class the network
        # predicts, and which class is the labeled class:
        test_results = [(np.argmax(self.feedforward(x)), np.argmax(y)) for
                        (x, y) in test_data]
        if accuracy:
        	# Compare predicted and observed labels:
            return sum(int(y_pred == y) for (y_pred, y) in test_results)
        else:
        	# Return probabilities associated with each neuron, rather than
        	# returning labels:
            return [self.feedforward(x) for (x, y) in test_data]

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives of quadratic cost function.
        """
        return output_activations-y
