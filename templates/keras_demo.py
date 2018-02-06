import numpy as np
from PIL import Image
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image as keras_image
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg, \
    decode_predictions as decode_predictions_vgg

  
class ModelInterface():
  
  def __init__(self):
    self.model = VGG16(weights='imagenet')


  ### Input: [+224, +224, 3]
  def prediction(self, input):
    img = Image.fromarray(input["image"])
    img = img.resize((224, 224))
    x = keras_image.img_to_array(img)[:, :, :3]
    x = np.expand_dims(x, axis=0)
    x = preprocess_input_vgg(x)
    features = self.model.predict(x)
    predictions = decode_predictions_vgg(features)[0]
    
    return {
      "predictions": [
        { 'score': k, 'class': j } for (i, j, k) in predictions
      ]
    }
  
  
  def test_image(self):
    img = Image.open("cat.jpg")
    img.load()
    img.thumbnail((512, 512), Image.ANTIALIAS)
    return np.array(img)

 
if __name__ == "__main__":   
  interface = ModelInterface()
  print(interface.prediction({
    "image": interface.test_image()
  }))