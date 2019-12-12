import tensorflow as tf


class Conv2D(object):

    def __init__(self,
                 kernel_shape,
                 num_kernels,
                 in_channels,
                 strides,
                 activation_fn=tf.nn.relu,
                 kernel_initializer=tf.initializers.GlorotUniform,
                 bias_initializer=tf.initializers.GlorotUniform
                 ):

        # If the provided kernel is only n,
        # expand to make kernel shape n x n
        if len(kernel_shape) == 1:
            kernel_shape = (kernel_shape, kernel_shape)

        self.kernel_shape = kernel_shape

        # Initialize kernels (filters)
        self.kernel = WeightVariable((kernel_shape[0],
                                      kernel_shape[1],
                                      in_channels,
                                      num_kernels),
                                      initializer=kernel_initializer,
                                     )

        # Initializee bias
        self.bias = BiasVariable((num_kernels),
                                 initializer=bias_initializer
                                 )


        # If the provided stride is only n,
        # expand to make stride n x n
        if len(strides) == 1:
            strides = (strides, strides)

        self.stride = strides

        self.activation_fn = activation_fn


    def call(self, x):

        # Perform convolution operation
        # TODO: figure out how to do this yourself in C++... might be an
        #       interesting side project
        feature_map = tf.nn.conv2d(x,
                                   self.kernel,
                                   strides=self.strides,
                                   padding='SAME'
                                   )
        # Add bias
        feature_map_biased = tf.bias_add(feature_map, self.bias)

        # Return activated feature map
        return self.activation_fn(feature_map_biased)


class WeightVariable(object):
    """
    Base class for weight parameters to be used in learning layers
    """
    def __init__(self,
                 shape,
                 name,
                 model_scope,
                 initializer=None):

        self.shape = shape
        self.name = name
        self.model_scope = model_scope
        self.initialize = initializer

    def call(self):

        with tf.variable_scope(self.model_scope, reuse=tf.AUTO_REUSE):
            initial = tf.get_variable(self.name, self.shape,
                                      initializer=self.initializer,
                                      trainable=True)
            variable_summaries(initial)

        return initial

class BiasVariable(object):
    """
    Base class for bias parameters to be used in learning layers
    """
    def __init__(self,
                 shape,
                 name,
                 model_scope,
                 initializer=None):

        self.shape = shape
        self.name = name
        self.model_scope = model_scope
        self.initializer = initializer

    def call(self):

        with tf.variable_scope(self.model_scope, reuse=tf.AUTO_REUSE):
            initial = tf.get_variable(self.name, self.shape,
                                      intiializer=self.initializer,
                                      trainable=True)
            variable_summaries(initial)

        return initial


def variable_summaries(var):
    """
    Method for saving summary statistics to TensorBoard
    """
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)

        with tf.name_scope('std_dev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))

        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)



