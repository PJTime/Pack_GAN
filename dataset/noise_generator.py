"""
Manufactures batches of noise, i.e., vectors of randomly distributed
numbers between 0 and 1, to feed into the generator
"""

import tensorflow as tf
import numpy as np

class NoiseGenerator(object):

    def __init__(self,
                 image_height,
                 image_width,
                 num_channels,
                 num_tags,
                 latent_space_vector_dim,
                 batch_size=4,
                 num_threads=1,
                 prefetch_batch_buffer=30,
                 encoding_function=None,
                 ):

        self.num_channels = num_channels
        #dimension of vector randomly sampled from latent space
        #that is going to be fed into the generator
        self.num_tags = num_tags
        self.latent_space_vector_dim = latent_space_vector_dim
        self.batch_size = batch_size
        self.num_threads = num_threads
        self.prefetch_batch_buffer = prefetch_batch_buffer
        self.encoding_function = encoding_function

    def build_pipeline(self,
                       latent_space_vector_dim,
                       num_tags,
                       preprocess=False,
                       ):

        data = tf.data.Dataset.from_generator(self.generate_random_noise(
            latent_space_vector_dim, num_tags))

        # Perform additional preprocessing to generated noise
        if preprocess:
            # TODO: add preprocessing steps, if you think that is necessary
            pass

        data = data.repeat()

        # batch data
        data = data.batch(batch_size)






    def generate_random_noise(self, latent_space_vector_dim, num_tags):
        """
        :param latent_space_vector_dim: dimension of vector randomly
                                        sampled from latent space
                                        that is going to be fed into
                                        the generator

        :return random_uniform_batch: tensor of randomly generated values
                                      in set [0,1] with dtype tf.float32

                                      shape: (latent_space_vector_dim, )

        :return random_uniform_tags: generate a tensor of random uniform noise
                                     with same dimension as tags ( the reason
                                     that we are keeping these tensors seperate
                                     for now is that we will need to keep track
                                     of what tags we randomly assigned to the
                                     tensor we generate from latent space
        """
        latent_space_image_noise = tf.random.uniform((latent_space_vector_dim,),
                                                     minval=-1.0, maxval=1.0,
                                                     dtype=tf.dtypes.float32)

        latent_space_tag_noise = tf.random.uniform((num_tags,),
                                                   minval=-1.0, maxval=1.0,
                                                   dtype=tf.dtypes.float32)

        return latent_space_image_noise, latent_space_tag_noise




    def get_iterator(self):
        # Create and return iterator
        return self.dataset.make_one_shot_iterator()
