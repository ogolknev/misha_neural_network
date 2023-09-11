import random
import os
from pathlib import Path

class Neuron:
    def __init__(self, synapses_num) -> None:
        self.weight = list()
        self.weight.append(random.random())
        for _ in range(1, synapses_num + 1):
            self.weight.append(random.random())

    def activate(self, input: list):
        if len(input) != len(self.weight) - 1:
            raise Exception('mismatch in the number of inputs!')
        s = self.weight[0]
        for i in range(len(input)):
            s += input[i] * self.weight[i + 1]
        if s > 0:
            return 1
        return 0

    def learning(self, input: list, output, n):
        output_ = self.activate(input)
        if output == output_:
            return 1
        self.weight[0] = self.weight[0] + n * 1 * (output - output_)
        for i in range(1, len(self.weight)):
            self.weight[i] = self.weight[i] + n * input[i - 1] * (output - output_)
        return 0

    
class Layer():
    def __init__(self, neurons_num = None, synapses_num = None, *neurons: Neuron) -> None:
        if neurons:
            self.neurons = neurons
            self.neurons_num = len(neurons)
        elif neurons_num:
            self.neurons = list()
            self.neurons_num = neurons_num
            for _ in range(neurons_num):
                self.neurons.append(Neuron(synapses_num))

    def activate(self, input: list):
        output = list()
        for neuron in self.neurons:
            output.append(neuron.activate(input))
        return output
    
    def save(self):
        saves_folder = Path('saves')
        if not os.path.exists('saves'):
            os.mkdir('saves')
        save = open(f'saves/save_{self.neurons_num}_{len(self.neurons[0].weight)}_{len(list(saves_folder.iterdir()))}.txt', 'w')
        for i in range(self.neurons_num):
            save_line = ''
            for j in range(len(self.neurons[0].weight)):
                save_line += str(self.neurons[i].weight[j])+'|'
            save.write(save_line + '\n')
        save.close()
    
    def load(self, path: str):
        save = open(path, 'r')
        for i in range(self.neurons_num):
            line = save.readline()[:-2].split('|')
            self.neurons[i].weight = list((float(x) for x in line))
        save.close()

    
def learning(layer:Layer, training_sample: list, n):
    switch = True
    counter = 0
    while switch:
        counter += 1;
        counter_ = 0;
        for i in range(layer.neurons_num):
            for j in range(len(training_sample[0])):
                for k in range(len(training_sample[0][j])):
                    counter_ += layer.neurons[i].learning(training_sample[0][j][k], training_sample[1][k][i], n)
        print(counter_)
        print(len(training_sample[0]) * len(training_sample[1][0]) * len(training_sample[0][0]))
        print()
        if counter_ == len(training_sample[0]) * len(training_sample[1][0]) * len(training_sample[0][0]):
            switch = False
    return counter

def p_learning(layer:Layer, training_p: list, n):
    switch = True
    counter = 0
    while switch:
        counter += 1;
        counter_ = 0;
        for i in range(layer.neurons_num):
                    counter_ += layer.neurons[i].learning(training_p[0], training_p[1][i], n)
        if counter_ == layer.neurons_num:
            switch = False
    return counter


def out_decode(out):
    for i in range(len(out)):
            if out[i] == 1:
                return i
    return None

def out_encode(out, num):
    out_l = list()
    for i in range(num):
        if i == out:
            out_l.append(1)
        else:
            out_l.append(0)
    return out_l