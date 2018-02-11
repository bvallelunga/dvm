import base64, io, codecs, json
import numpy as np
from PIL import Image
from keras import backend
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image as keras_image
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg, \
    decode_predictions as decode_predictions_vgg

  
class ModelInterface():
  
  def __init__(self):
    self.model = VGG16(weights='imagenet')


  ### Input: 3d array
  def prediction(self, input):  
    data = np.array(input["image"], dtype=np.uint8)
    
    json.dump({
      "input": {
        "image": data.tolist()
      }
    }, codecs.open("input.json", 'w', encoding='utf-8'), separators=(',', ':'))
    
    img = Image.fromarray(data)
    img = img.resize((224, 224))
    x = keras_image.img_to_array(img)[:, :, :3]
    x = np.expand_dims(x, axis=0)
    x = preprocess_input_vgg(x)
    features = self.model.predict(x)
    predictions = decode_predictions_vgg(features)[0]
    backend.clear_session()
    
    return {
      "predictions": [
        { 'score': k, 'class': j } for (i, j, k) in predictions
      ]
    }
  
  
  def test_image(self):
    img = Image.open("cat.jpg")
    img.load()
    img.thumbnail((512, 512), Image.ANTIALIAS)
    return np.array(img).tolist()

 
if __name__ == "__main__":   
  interface = ModelInterface()
  print(interface.prediction({
    "image": interface.test_image()
  }))