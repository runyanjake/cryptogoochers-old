#special imports for using things that will be in python in the future.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

#starting values and input layer
starting_values = [[1], [2], [3], [4]]
input = tf.constant(starting_values, tf.float32)
#expeted value
expected_values = [[9], [9], [9], [9]]
goal = tf.constant(expected_values, tf.float32)
#create linear model with a single output
model = tf.layers.Dense(units=1)
#process to calculate loss
guess = model(starting_values)
loss = tf.losses.mean_squared_error(labels=goal, predictions=guess)
#setup optimization/training techniques
learn_rate = 0.01
optimizer = tf.train.GradientDescentOptimizer(learn_rate)
train = optimizer.minimize(loss)
#initialize network
init = tf.global_variables_initializer()

#run the network
sess = tf.Session()
sess.run(init)
for i in range(1,100):
    _, loss_val = sess.run((train, loss))
    print("Loss value at iteration " + str(i) + ": " + str(loss_val))

print("Final Network value: " + str(sess.run(guess)))