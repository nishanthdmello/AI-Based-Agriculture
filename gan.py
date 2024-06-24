import numpy as np
import tensorflow as tf # type: ignore
from tensorflow.keras import layers, Model # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pandas as pd

data_df = pd.read_csv('crop_fertilizers.csv')

original_data = {
    'temperature': data_df['Temperature'].values,
    'humidity': data_df['Humidity'].values,
    'rainfall': data_df['Rainfall'].values,
    'nitrogen': data_df['Nitrogen'].values,
    'phosphorus': data_df['Phosphorus'].values,
    'potassium': data_df['Potassium'].values,
    'moisture': data_df['Moisture'].values,
    'pH': data_df['pH'].values,
}

# Normalize the data
temperature_mean, temperature_std = np.mean(original_data['temperature']), np.std(original_data['temperature'])
humidity_mean, humidity_std = np.mean(original_data['humidity']), np.std(original_data['humidity'])
rainfall_mean, rainfall_std = np.mean(original_data['rainfall']), np.std(original_data['rainfall'])
nitrogen_mean, nitrogen_std = np.mean(original_data['nitrogen']), np.std(original_data['nitrogen'])
phosphorus_mean, phosphorus_std = np.mean(original_data['phosphorus']), np.std(original_data['phosphorus'])
potassium_mean, potassium_std = np.mean(original_data['potassium']), np.std(original_data['potassium'])
moisture_mean, moisture_std = np.mean(original_data['moisture']), np.std(original_data['moisture'])
pH_mean, pH_std = np.mean(original_data['pH']), np.std(original_data['pH'])

normalized_temperature = (original_data['temperature'] - temperature_mean) / temperature_std
normalized_humidity = (original_data['humidity'] - humidity_mean) / humidity_std
normalized_rainfall = (original_data['rainfall'] - rainfall_mean) / rainfall_std
normalized_nitrogen = (original_data['nitrogen'] - nitrogen_mean) / nitrogen_std
normalized_phosphorus = (original_data['phosphorus'] - phosphorus_mean) / phosphorus_std
normalized_potassium = (original_data['potassium'] - potassium_mean) / potassium_std
normalized_moisture = (original_data['moisture'] - moisture_mean) / moisture_std
normalized_pH = (original_data['pH'] - pH_mean) / pH_std

# Prepare data for training
data = np.vstack((normalized_temperature, normalized_humidity)).T
dataset = tf.data.Dataset.from_tensor_slices(data).shuffle(50).batch(50)

# Generator
def make_generator_model():
    model = tf.keras.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=(2,)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(2, activation='tanh'))
    return model

# Discriminator
def make_discriminator_model():
    model = tf.keras.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=(2,)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model

generator = make_generator_model()
discriminator = make_discriminator_model()

# Loss function and optimizers
cross_entropy = tf.keras.losses.BinaryCrossentropy()
generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

# Training the GAN
@tf.function
def train_step(data, batch_size):
    noise = tf.random.normal([batch_size, 2])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_data = generator(noise, training=True)

        real_output = discriminator(data, training=True)
        fake_output = discriminator(generated_data, training=True)

        gen_loss = cross_entropy(tf.ones_like(fake_output), fake_output)
        disc_loss_real = cross_entropy(tf.ones_like(real_output), real_output)
        disc_loss_fake = cross_entropy(tf.zeros_like(fake_output), fake_output)
        disc_loss = disc_loss_real + disc_loss_fake

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

def train(dataset, epochs, batch_size):
    for epoch in range(epochs):
        for data_batch in dataset:
            train_step(data_batch, batch_size)
        if epoch % 100 == 0:
            print(f'Epoch {epoch} completed')

# Training parameters
EPOCHS = 2000
BATCH_SIZE = 50

# Training the GAN
train(dataset, EPOCHS, BATCH_SIZE)

# Generating synthetic data
synthetic_data = generator(tf.random.normal([200, 2])).numpy()

# Denormalizing synthetic data
synthetic_temperature = synthetic_data[:, 0] * temperature_std + temperature_mean
synthetic_humidity = synthetic_data[:, 1] * humidity_std + humidity_mean

# Plotting synthetic data
plt.scatter(synthetic_temperature, synthetic_humidity, label='Synthetic Data')
plt.scatter(original_data['temperature'], original_data['humidity'], label='Original Data')
plt.xlabel('Temperature')
plt.ylabel('Humidity')
plt.legend()
plt.show()
