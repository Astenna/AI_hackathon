import numpy as np
import tensorflow as tf
import pandas as pd
import json

# read trained model
stock_pred_model = tf.keras.models.load_model("models/model.h5")

# load inference data
inference_data = pd.read_csv(
    "datasets/inference/prepared/inference_data.csv", sep=",", header=None
).values

date = []
input_values = []
input_vector = []

date.append(inference_data[-1, 0])
input_values.append(inference_data[-1, 1:7])
input_vector.append(
    np.array(
        [
            inference_data[-1, 7],
            inference_data[-2, 7],
            inference_data[-3, 7],
            inference_data[-4, 7],
            inference_data[-5, 7],
        ]
    ).reshape((5, 1))
)

input_values = np.array(input_values)
input_vector = np.array(input_vector)

# predict
prediction = stock_pred_model.predict([input_vector, input_values])

# date from csv!
def get_predict_json(date, prediction):
    """
 Function that returns json with predictions.
 :param prediction: (np.array)
 :return: json
 """
    increase = np.round(prediction[0][0], 5)
    decrease = np.round(prediction[0][1], 5)
    data = {
        "date": date,
        "prediction": {"increase": str(increase), "decrease": str(decrease)},
    }
    return data


prediction_json = get_predict_json(date=date[0], prediction=prediction)
try:
    with open("predictions/prediction.json", "r") as json_file:
        pred = json.load(json_file)
except (IOError, json.decoder.JSONDecodeError):
    pred = []
pred.append(prediction_json)
with open("predictions/prediction.json", "w") as json_file:
    json.dump(pred, json_file, indent=4)
