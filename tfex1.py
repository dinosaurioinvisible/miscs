
import tensorflow as tf
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout 

mnist = tf.keras.datasets.mnist

(xtrain,ytrain), (xtest,ytest) = mnist.load_data()

print(f'\nxtrain: {xtrain.shape}, xtest={xtest.shape}\n')

# colors to 0-1
xtrain, xtest = xtrain/255, xtest/255

model = Sequential([
    Input(shape=(28,28)),
    Flatten(),
    Dense(128,activation='relu'),
    Dropout(0.2),
    Dense(10)
])

pxs = model(xtrain[:1]).numpy()

# sample predictions
# print(pxs)

# as probs
# print(tf.nn.softmax(pxs).numpy())

loss_fx = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(
    optimizer='adam',
    loss=loss_fx,
    metrics=['accuracy'])

model.fit(xtrain,ytrain,epochs=2)

print()
model.evaluate(xtest,ytest,verbose=2)

# as probs
pmodel = Sequential([
    model,
    tf.keras.layers.Softmax()
])

print()
for i in range(5):
    txi = pmodel(xtest[:5])[i].numpy()
    conf = round(txi.max()*100,2)
    print(f'prediction: {txi.argmax()},  conf: {conf:.2f}%, correct: {ytest[i]}')
print()

