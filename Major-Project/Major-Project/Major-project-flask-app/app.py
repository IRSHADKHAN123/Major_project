from flask import Flask, request, jsonify
from utils.feature_extraction import calculate_features
from utils.config import CIPHERTYPES
import tensorflow as tf
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_keys_from_value(value):
    keys = [key for key, val in CIPHERTYPES.items() if val == value]
    return keys

def load_models():
    models = {}
    models['knn'] = pickle.load(open('./saved_models/knn.pkl', 'rb'))
    models['gbc'] = pickle.load(open('./saved_models/gbc.pkl', 'rb'))
    models['GaussianNB'] = pickle.load(open('./saved_models/GaussianNB.pkl', 'rb'))
    models['randomforest'] = pickle.load(open('./saved_models/randomforest.pkl', 'rb'))
    models['svc'] = pickle.load(open('./saved_models/svc.pkl', 'rb'))
    models['ffn'] = tf.keras.models.load_model("./saved_models/ffn.keras")
    return models

models = load_models()

@app.route('/ciphertype', methods=['GET'])
def predict_ciphertype():
    ciphertext = request.args.get('ciphertext')
    if len(ciphertext) < 100:
        return jsonify({'error': 'Ciphertext length should be at least 100 characters'})
    
    feature = calculate_features(ciphertext.encode())
    result = []
    for name, model in models.items():
        if name == 'ffn':
            print("hello ffn here \n\n")
            feature = np.array(feature)
            feature = feature.reshape(1, -1)
            prediction = model.predict(feature)
            prob = prediction.max(axis=1)[0]
            cipher_index = np.argmax(prediction[0])
            # print("name",name,"cipher_index",cipher_index,"cipher_type",cipher_type)

        else:
            prediction = model.predict([feature])
            prob = model.predict_proba([feature]).max(axis=1)[0]
            cipher_index = prediction[0]
        
        cipher_type = get_keys_from_value(cipher_index)
        # print(models)
        # print(name,model,cipher_index,cipher_type)
        # result.append({'model_name': name, 'cipher_type': cipher_type, 'probability': prob})
        result.append({'model_name': name, 'cipher_type': cipher_type, 'probability': float(prob)})


    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
