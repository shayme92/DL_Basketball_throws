from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Model

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from RunGame import mainGame
from Consts import Consts
C = Consts()

# Load the throws data
df = pd.read_csv('throwData.csv')

# Allocate the data to corresponding variables
X_org = np.array([df['x'], df['y'], df['angle']]).T
angles = np.array([df['angle']]).T
positions = np.array([df['x'], df['y']]).T

# Predict to V for each position
Y = np.array([df['velocity']]).T

# Change X positions to polar coordinates
X = np.zeros((X_org.shape[0],2))
for i,x in enumerate(X_org):
    dist = np.linalg.norm([x[0],x[1]]-C.HOOP_CENTER_POINT)
    if (x[0]<(C.HOOP_X-140)):
        X[i,0] = dist
        X[i,1] = X_org[i,2]

## Split to train test by train_size_prcnt
N_samples = X.shape[0]
train_size_prcnt = 0.7
train_indices = np.arange(round(N_samples*train_size_prcnt))
test_indices = np.arange(round(N_samples*train_size_prcnt),N_samples)

X_train = X[train_indices, :]
X_test  = X[test_indices, :]
Y_train = Y[train_indices, :]
Y_test  = Y[test_indices, :]

## NN modal define
input = Input(shape=(2,))
hidden_layer_1 = Dense(20, activation='relu')(input)
hidden_layer_2 = Dense(20, activation='relu')(hidden_layer_1)
hidden_layer_3 = Dense(20, activation='relu')(hidden_layer_2)
hidden_layer_4 = Dense(20, activation='relu')(hidden_layer_3)
output = Dense(1)(hidden_layer_4)
model = Model(inputs=input, outputs=output)
model.compile(
    optimizer='adam',
    loss=['mean_squared_error']
)
## Fit NN by train
history = model.fit(X_train, Y_train, epochs=3000, batch_size=200,
                        validation_data=(X_test, Y_test)
                        )

# Predict using test samples ("new throws")
result = model.predict(X_test[:,:])

# Get training and test loss histories
training_loss = history.history['loss']
test_loss = history.history['val_loss']

# Create count of the number of epochs
epoch_count = range(1, len(training_loss) + 1)

# Visualize loss history
plt.plot(epoch_count, training_loss, 'r--')
plt.plot(epoch_count, test_loss, 'b-')
plt.legend(['Training Loss', 'Test Loss'])
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()

# Set game inputs for predictions evaluation
pos_vec = positions[test_indices,:]
velocity_vec, angle_vec = result[:, 0], angles[test_indices, :]
df = pd.DataFrame(data={'x': pos_vec[:,0],'y': pos_vec[:,1], 'velocity_vec': velocity_vec, 'angle_vec': angle_vec[:,0]})

# Save locally the new throws data base
df.to_csv('new_throws_prediction_data2.csv')

# Run game with predictions
mainGame(pos_vec.tolist(), velocity_vec, angle_vec, 10000)
