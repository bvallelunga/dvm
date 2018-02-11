import io, base64
import numpy as np
from PIL import Image
from decimal import Decimal
import requests
from torch.autograd import Variable
import torchvision.models as models
from torch.nn.functional import softmax
import torchvision.transforms as transforms


class ModelInterface():
  
  NAME = ("VG16." + __name__)
  TEST_IMG_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg'
  LABELS_URL = 'https://s3.amazonaws.com/outcome-blog/imagenet/labels.json'
  
  image_size = 224
  output_limit = 10
  
  def __init__(self):
    self._fetchModel()
    self._fetchLabels()
    print(self.NAME, "Finished Setup")
    
  
  def _fetchModel(self):
    print(self.NAME, "Loading Model")
    self.model = models.vgg16(pretrained=True)
    self.model.eval()
  
    
  def _fetchLabels(self):
    print(self.NAME,  "Loading Labels")
    response = requests.get(self.LABELS_URL)
    self.labels = {int(key): value for key, value in response.json().items()}
    
  
  def _testImage(self):
    response = requests.get(self.TEST_IMG_URL)
    img_stream = io.BytesIO(response.content)
    return base64.encodestring(img_stream.read()).decode("utf-8")
    
    
  # Input: Base64 encoded string
  def prediction(self, input): 
    img_byte_string = base64.decodestring(input["image"].encode())
    img = Image.open(io.BytesIO(img_byte_string))
    
    # Now that we have an img, we need to preprocess it.
    # We need to:
    #       * resize the img, it is pretty big (~1200x1200px).
    #       * normalize it, as noted in the PyTorch pretrained models doc,
    #         with, mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225].
    #       * convert it to a PyTorch Tensor.
    #
    # We can do all this preprocessing using a transform pipeline.
    min_img_size = 224  # The min size, as noted in the PyTorch pretrained models doc, is 224 px.
    transform_pipeline = transforms.Compose([transforms.Resize(self.image_size),
                                             transforms.ToTensor(),
                                             transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                  std=[0.229, 0.224, 0.225])])
    img = transform_pipeline(img)
    
    # PyTorch pretrained models expect the Tensor dims to be (num input imgs, num color channels, height, width).
    # Currently however, we have (num color channels, height, width); let's fix this by inserting a new axis.
    img = img.unsqueeze(0)  # Insert the new axis at index 0 i.e. in front of the other axes/dims. 
    
    # Now that we have preprocessed our img, we need to convert it into a 
    # Variable; PyTorch models expect inputs to be Variables. A PyTorch Variable is a  
    # wrapper around a PyTorch Tensor.
    img = Variable(img)
    
    # Now let's load our model and get a prediciton!
    predictions = self.model(img) # Returns a Tensor of shape (batch, num class labels)
    scores = softmax(predictions, dim=1).data.numpy().reshape(-1)
    top_classes = 5  # The top k classes to select.
    indicies = np.argpartition(scores, -top_classes)[-top_classes:]
    results = [{'label': self.labels[i].lower(), 'score': Decimal(str(scores[i]))} for i in indicies]
    return {
      "predictions": sorted(results, key=lambda result: result["score"], reverse=True)
    }


if __name__ == "__main__":
  interface = ModelInterface()
  print(interface.prediction({
    "image": interface._testImage()
  }))
  