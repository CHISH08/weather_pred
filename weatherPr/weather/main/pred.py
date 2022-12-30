import tensorflow as tf
import numpy as np

# Поведенческий паттерн(Цепочка обязанностей(chain of responsibility)): class по поданным в него dataframe
# предсказывает погоду на завтра
class NN_pred:
    def __init__(self,X,dr,feature_cols):
        self.X = X
        self.dr = dr
        self.feature_cols = feature_cols
    def wx_input_fn(self, y=None, num_epochs=None, shuffle=True, batch_size=400):
        return tf.compat.v1.estimator.inputs.pandas_input_fn(x=self.X,
                                                   y=y,
                                                   num_epochs=num_epochs,
                                                   shuffle=shuffle,
                                                   batch_size=batch_size)

    def pred(self):
        regressor = tf.estimator.DNNRegressor(feature_columns=self.feature_cols,
                                              hidden_units=[50, 50],
                                              model_dir=self.dr)
        pred = regressor.predict(input_fn=self.wx_input_fn(self.X,
                                                      num_epochs=1,
                                                      shuffle=False))
        return np.array([p['predictions'][0] for p in pred])[0]