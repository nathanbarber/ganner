import tensorflow as tf
import numpy as np
import skimage
import os

class Ganner:
    def __init__(self, dim, train_range, out_step, pack_path):
        self.dim = dim
        self.tr = train_range
        self.out_step = out_step
        self.data = []
        self.completed = []
        self.pack_path = pack_path
        for i in os.listdir(pack_path):
            self.data.append(
                skimage.io.imread(pack_path + i))
        self.train = np.array(self.data)
        print(np.shape(self.train))

    def xavier_init(self, size):
        in_dim = size[0]
        xavier_stddev = 1. / tf.sqrt(in_dim / 2.)
        return tf.random_normal(shape=size, stddev=xavier_stddev)

    def sample_Z(self, m, n):
            return np.random.uniform(-1., 1., size=[m, n])

    def plot(self, samples):
        fig = plt.figure(figsize=(4, 4))
        gs = gridspec.GridSpec(4, 4)
        gs.update(wspace=0.05, hspace=0.05)

        for i, sample in enumerate(samples):
            ax = plt.subplot(gs[i])
            plt.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_aspect('equal')
            plt.imshow(sample.reshape(28, 28), cmap='Greys_r')

        return fig

    def choose_batch(self, size):
        rands = []
        ds_len = np.shape(self.train)[0]
        for i in range(size):
            rands.append(
                np.random.randint(0, ds_len)
            )
        return rands

    def Generate(self):
        X = tf.placeholder(tf.float32, shape=[None, self.dim, 3])j
        D_W1 = tf.Variable(self.xavier_init([self.dim, 128, 3]))
        D_B1 = tf.Variable(tf.zeros(shape=[128]))
        D_W2 = tf.Variable(self.xavier_init([128, 1]))
        D_B2 = tf.Variable(tf.zeros(shape=[1]))

        theta_d = [D_W1, D_W2, D_B1, D_B2]

        Z = tf.placeholder(tf.float32, shape=[None, 100])
        G_W1 = tf.Variable(self.xavier_init([100, 128]))
        G_B1 = tf.Variable(tf.zeros(shape=[128]))
        G_W2 = tf.Variable(self.xavier_init([128, self.dim]))
        G_B2 = tf.Variable(tf.zeros(shape=[self.dim]))

        theta_g = [G_W1, G_W2, G_B1, G_B2]

        def generator(z):
            G_h1 = tf.nn.relu(tf.matmul(z, G_W1) + G_B1)
            G_log_prob = tf.matmul(G_h1, G_W2) + G_B2
            G_prob = tf.nn.sigmoid(G_log_prob)

            return G_prob

        def discriminator(x):
            D_h1 = tf.nn.relu(tf.matmul(x, D_W1) + D_B1)
            D_logit = tf.matmul(D_h1, D_W2) + D_B2
            D_prob = tf.nn.sigmoid(D_logit)

            return D_prob, D_logit

        G_sample = generator(Z)
        D_real, D_logit_real = discriminator(X)
        D_fake, D_logit_fake = discriminator(G_sample)

        # Alt loss
        D_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_logit_real, labels=tf.ones_like(D_logit_real)))
        D_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_logit_fake, labels=tf.zeros_like(D_logit_fake)))
        D_loss = D_loss_real + D_loss_fake
        G_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_logit_fake, labels=tf.ones_like(D_logit_fake)))

        D_solver = tf.train.AdamOptimizer().minimize(D_loss, var_list=theta_d)
        G_solver = tf.train.AdamOptimizer().minimize(G_loss, var_list=theta_g)

        mb_size = 3
        Z_dim = 100

        # Replacing with packer data
        mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
        data = self.train

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            # Create outdir
            if not os.path.exists("out/"):
                os.mkdir("out/")

            # Train / create loop
            i = 0
            for it in range(self.tr):
                # Create outstep
                if it % self.out_step == 0:
                    print("Outstep %s", it)
                    samples = sess.run(G_sample, feed_dict={Z: self.sample_Z(16, Z_dim)})

                    fig = self.plot(samples)
                    plt.savefig('out/{}.png'.format(str(i).zfill(3)), bbox_inches='tight')
                    i += 1

                batch = []
                select = self.choose_batch(mb_size)
                for i in select:
                    batch.append(self.train[i])
                X_mb, _ = batch

                _, D_loss_curr = sess.run([D_solver, D_loss], feed_dict={X: X_mb, Z: self.sample_Z(mb_size, Z_dim)})
                _, G_loss_curr = sess.run([G_solver, G_loss], feed_dict={Z: self.sample_Z(mb_size, Z_dim)})

                if it % self.out_step == 0:
                    print('D loss: {:.4}'. format(D_loss_curr))
                    print('G_loss: {:.4}'. format(G_loss_curr))
                    print()