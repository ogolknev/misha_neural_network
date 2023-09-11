import neural_network as nn
from training_sample import training_sample as ts
from time import sleep

n_net = nn.Layer(10,35)

nn.learning(n_net, ts.ts_init("lab1/training_sample"), 0.1)

print(n_net.activate(ts.img_cnvrt('lab1/training_sample/input/set0/2.png')))


n_net.load('C:/Users/ogolknev/development/projects/artificial-neural-networks/saves/save_10_36_0.txt')
n_net.save()

# ts.test()
