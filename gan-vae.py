import numpy as np
import matplotlib.pyplot as plt # type: ignore
import tensorflow as tf # type: ignore
from tensorflow.keras import layers, Model # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
import pandas as pd

# Load data
data_df = pd.read_csv('crop_fertilizers.csv')

original_data = {
    'temperature': data_df['Temparature'].values,
    'humidity': data_df['Humidity '].values
}

# Normalize the data
scaler = StandardScaler()
normalized_data = scaler.fit_transform(np.vstack((original_data['temperature'], original_data['humidity'])).T)

# VAE Model
latent_dim = 2

# Custom Sampling Layer
class Sampling(layers.Layer):
    def call(self, inputs):
        z_mean, z_log_var = inputs
        epsilon = tf.keras.backend.random_normal(shape=(tf.keras.backend.shape(z_mean)[0], latent_dim), mean=0., stddev=1.)
        return z_mean + tf.keras.backend.exp(0.5 * z_log_var) * epsilon

# Encoder
encoder_inputs = layers.Input(shape=(2,))
x = layers.Dense(16, activation='relu')(encoder_inputs)
z_mean = layers.Dense(latent_dim)(x)
z_log_var = layers.Dense(latent_dim)(x)
z = Sampling()([z_mean, z_log_var])

encoder = Model(encoder_inputs, [z_mean, z_log_var, z])

# Decoder
latent_inputs = layers.Input(shape=(latent_dim,))
x = layers.Dense(16, activation='relu')(latent_inputs)
outputs = layers.Dense(2)(x)

decoder = Model(latent_inputs, outputs)

# Custom VAE Model
class VAE(Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def call(self, inputs):
        z_mean, z_log_var, z = self.encoder(inputs)
        reconstructed = self.decoder(z)
        
        # Add KL divergence regularization loss
        kl_loss = -0.5 * tf.reduce_mean(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
        self.add_loss(kl_loss)
        return reconstructed

vae = VAE(encoder, decoder)

# Compile the VAE
vae.compile(optimizer='adam', loss='mse')

# GAN Model
generator_input = layers.Input(shape=(latent_dim,))
x = layers.Dense(16, activation='relu')(generator_input)
generator_output = layers.Dense(2)(x)

generator = Model(generator_input, generator_output)

discriminator_input = layers.Input(shape=(2,))
x = layers.Dense(16, activation='relu')(discriminator_input)
discriminator_output = layers.Dense(1, activation='sigmoid')(x)

discriminator = Model(discriminator_input, discriminator_output)

# Compile the discriminator
discriminator.compile(optimizer='adam', loss='binary_crossentropy')

# Freeze discriminator during combined model training
discriminator.trainable = False

# Combined VAE-GAN model
gan_input = layers.Input(shape=(latent_dim,))
gan_output = discriminator(generator(gan_input))
gan = Model(gan_input, gan_output)

# Compile the GAN
gan.compile(optimizer='adam', loss='binary_crossentropy')

# Training parameters
epochs = 2000
batch_size = 50

# Training the VAE
vae.fit(normalized_data, normalized_data, epochs=200, batch_size=batch_size, verbose=0)

# Training the GAN
for epoch in range(epochs):
    noise = np.random.normal(0, 1, (batch_size, latent_dim))
    generated_data = generator.predict(noise)
    real_data = normalized_data[np.random.randint(0, normalized_data.shape[0], batch_size)]
    combined_data = np.concatenate([real_data, generated_data])

    labels_real = np.ones((batch_size, 1))
    labels_fake = np.zeros((batch_size, 1))
    labels_combined = np.concatenate([labels_real, labels_fake])

    discriminator_loss = discriminator.train_on_batch(combined_data, labels_combined)

    noise = np.random.normal(0, 1, (batch_size, latent_dim))
    gan_loss = gan.train_on_batch(noise, np.ones((batch_size, 1)))

    if epoch % 100 == 0:
        print(f"Epoch: {epoch}, Discriminator Loss: {discriminator_loss}, GAN Loss: {gan_loss}")

# Generate synthetic data
synthetic_data = generator.predict(np.random.normal(0, 1, (200, latent_dim)))

# Denormalize synthetic data
synthetic_data = scaler.inverse_transform(synthetic_data)

# Plotting synthetic data
plt.scatter(synthetic_data[:, 0], synthetic_data[:, 1], label='Synthetic Data')
plt.scatter(original_data['temperature'], original_data['humidity'], label='Original Data')
plt.xlabel('Temperature')
plt.ylabel('Humidity')
plt.legend()
plt.show()