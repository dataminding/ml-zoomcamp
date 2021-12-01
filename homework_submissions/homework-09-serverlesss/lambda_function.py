from io import BytesIO
from urllib import request
from PIL import Image
import numpy as np
import tflite_runtime.interpreter as tflite


interpreter = tflite.Interpreter(model_path='cats-dogs-v2.tflite')
interpreter.allocate_tensors()
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]

TARGET_SIZE=(150,150)

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def preprocess_image(raw_img, target_size=TARGET_SIZE):
    img = prepare_image(raw_img, target_size)
    x = np.array(img, dtype='float32')
    # rescaling
    return x/255

def predict(url):
    raw_img = download_image(url)
    x = prepare_image(raw_img)
    X = np.array([x])
    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    proba = preds[0][0]
    specie = "dog" if proba>=0.5 else "cat"
    return {"result" : specie , "probability": str(proba), "preds":preds[0].tolist()}


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result

