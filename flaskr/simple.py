from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Dense
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
class Model():
    pass


class Simple(Model):
    def __init__(self, data, all_data = False):
        self.data = data
        self.model = Sequential([
            InputLayer(3),
            Dense(8, activation='sigmoid'),
            Dense(8, activation='sigmoid'),
            Dense(1, activation=tf.keras.activations.linear)
        ])

        self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])


        if all_data == False:
            self.train_set = self.data.iloc[:int(len(self.data)*0.8), :]
            self.test_set = self.data.iloc[int(len(self.data)*0.8):, :]
        else:
            self.train_set = self.data
            self.test_set = data.sample(frac = 0.2)
    def learn(self, epochs):
        result = []
        print(self.train_set[['Diff1', 'Diff2', 'Diff5']].values.shape)
        for epoch in range(epochs):
            self.model.fit(self.train_set[['Diff1', 'Diff2', 'Diff5']].values, self.train_set[['tomorrow']].values, batch_size=32, epochs=1)
            if self.test_set is not None:
                result.append(self.test())
        return result

    def test(self):
        predictions = self.model.predict(self.test_set[['Diff1', 'Diff2', 'Diff5']].values)
        predictions = [x[0] for x in predictions]
        return [self.__test_quantity(predictions), self.__test_mse(predictions)]

    def __test_quantity(self, predictions):
        results = []
        y_true = self.test_set["tomorrow"].values.tolist()
        for i, el in enumerate(predictions):
            if np.sign(el) == np.sign(y_true[i]):
                results.append(1)
            else:
                results.append(0)
        return np.sum(results) / len(predictions)

    def __test_mse(self,predictions):
        results = []
        y_true = self.test_set["tomorrow"].values.tolist()
        for i, el in enumerate(predictions):
            results.append(np.sqrt((el - y_true)**2))
        return np.average(results)
    def compare_predictions(self):
        pred = self.model.predict(self.test_set[['Diff1', 'Diff2', 'Diff5']].values)
        fig,ax = plt.subplots()
        ax.plot(self.test_set['tomorrow'].values)
        ax.plot(pred)
        print(pred)
        print(self.test_set['tomorrow'].values)
        ax.legend(['Actual', 'Predicted'])
        plt.show()
