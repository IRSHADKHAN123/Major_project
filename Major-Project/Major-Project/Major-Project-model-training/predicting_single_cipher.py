from generate_dataset.feature_extraction import calculate_features
from generate_dataset.config import CIPHERTYPES
import tensorflow as tf
import pickle
import numpy as np

def get_keys_from_value(value):
    key = [key for key, val in CIPHERTYPES.items() if val == value]
    return key

def get_ciphertext():
    ciphertext = input("Enter ciphertext:")
    if(len(ciphertext)<100):
        print("Enter ciphertext of minimum length  100")
        return None
    return ciphertext

def get_keys_from_value(value):
    keys = [key for key, val in CIPHERTYPES.items() if val == value]
    return keys[0]
def main():
    c = get_ciphertext()
    feature = calculate_features(c.encode())
    models = ['knn','gbc','randomforest','svc','GaussianNb','ffn']
    with open('./saved_models/knn.pkl','rb') as f:
        knn = pickle.load(f)
    with open('./saved_models/gbc.pkl','rb') as f:
        gbc = pickle.load(f)
    with open('./saved_models/GaussianNB.pkl','rb') as f:
        GaussianNB = pickle.load(f)
    with open('./saved_models/randomforest.pkl','rb') as f:
        randomforest = pickle.load(f)
    with open('./saved_models/svc.pkl','rb') as f:
        svc = pickle.load(f)
    ffn = tf.keras.models.load_model("./saved_models/ffn.keras")

    result = [0]*6
    r_prob = [0]*6
    result[0] = knn.predict([feature])
    r_prob[0] = knn.predict_proba([feature]).max(axis=1)[0]

    # print(result[0][np.argmax(result[0])],result[0],[np.argmax(result[0])])

    result[1] = gbc.predict([feature])
    r_prob[1] = gbc.predict_proba([feature]).max(axis=1)[0]

    result[2] = randomforest.predict([feature])
    r_prob[2] = randomforest.predict_proba([feature]).max(axis=1)[0]

    result[3] = svc.predict([feature])
    r_prob[3] = svc.predict_proba([feature]).max(axis=1)[0]

    result[4] = GaussianNB.predict([feature])
    r_prob[4] = GaussianNB.predict_proba([feature]).max(axis=1)[0]

    feature = np.array(feature)    
    feature = feature.reshape(1, -1)
    
    result[5] = ffn.predict(feature)
    r_prob[5] = result[5].max(axis=1)[0]
    result[5] = [np.argmax(result[5][0])]
    
    # print("prediction",result[5],"",)
    name_width = 20
    result_width = 20
    prob_width = 10
    print(f"{'Name of model':<{name_width}}: Cipher Type, {'Correctness probability':>{prob_width}}")
    for cipher_index,prob,name in zip(result,r_prob,models):
        # Format the print statement with fixed widths
        print(f"{name:<{name_width}}: {get_keys_from_value(cipher_index[0])} :  {prob:>{prob_width}}")

if __name__ == "__main__":
    main()