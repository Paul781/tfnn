import time
from sklearn.datasets import fetch_olivetti_faces
from sklearn.datasets import load_boston
from sklearn.linear_model import SGDClassifier
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
import tfnn
import numpy as np

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

tfnn.set_random_seed(100)

# xs = load_boston().data
# ys = load_boston().target
# xs = fetch_olivetti_faces().data
# ys = fetch_olivetti_faces().target[:, np.newaxis]

# xs = np.linspace(-5, 5, 300)[:, np.newaxis]
# ys = xs**2

# data = tfnn.Data(xs, ys)
# data.shuffle(inplace=True)
# data.to_binary(inplace=True)

network = tfnn.ClfNetwork(mnist.train.images.shape[1], mnist.train.labels.shape[1], do_dropout=False)
# network = tfnn.RegNetwork(data.xs.shape[1], data.ys.shape[1], do_dropout=True)
# norm_data = network.normalizer.minmax_fit(data)
# t_data, v_data = norm_data.train_test_split(0.7)

h1 = tfnn.HiddenLayer(100, activator='relu', dropout_layer=False)
h2 = tfnn.HiddenLayer(10, activator='tanh', dropout_layer=False)
out = tfnn.OutputLayer(activator=None, w_initial='random_normal')
network.build_layers([h1, h2, out])

optimizer = tfnn.train.GradientDescentOptimizer(0.01)
network.set_optimizer(optimizer)
evaluator = tfnn.Evaluator(network)
# write summarizer at the end of the structure
summarizer = tfnn.Summarizer(network, save_path='tmp',)

for i in range(1000):
    # b_xs, b_ys = t_data.next_batch(50, loop=True)
    b_xs, b_ys = mnist.train.next_batch(50)
    network.run_step(b_xs, b_ys, 0.5)
    if i % 50 == 0:
        # print(evaluator.compute_accuracy(v_data.xs, v_data.ys))
        # evaluator.plot_regression_linear_comparison(v_data.xs, v_data.ys, True)
        # evaluator.plot_regression_nonlinear_comparison(v_data.xs, v_data.ys, continue_plot=True)
        # print(evaluator.compute_cost(v_data.xs, v_data.ys))
        print(evaluator.compute_accuracy(b_xs, b_ys))
        summarizer.record_train(b_xs, b_ys, i, 0.5, )
        # evaluator.plot_instant_cost_r2(b_xs, b_ys, i, v_data.xs, v_data.ys)
        # evaluator.plot_instant_cost_r2(b_xs, b_ys, i, mnist.test.images, mnist.test.labels)
        # summarizer.record_test(v_data.xs, v_data.ys, i)
        # summarizer.record_test(mnist.test.images, mnist.test.labels, i)
# evaluator.hold_plot()
summarizer.web_visualize()
network.sess.close()


