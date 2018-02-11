"""
This script will demonstrate how to use a pretrained model, in PyTorch, 
to make predictions. Specifically, we will be using VGG16 with a cat 
image.
References used to make this script:
PyTorch pretrained models doc:
    http://pytorch.org/docs/master/torchvision/models.html
PyTorch image transforms example:
    http://pytorch.org/tutorials/beginner/data_loading_tutorial.html#transforms
Example code:
    http://blog.outcome.io/pytorch-quick-start-classifying-an-image/    
"""

import io
import base64

from PIL import Image
import requests

from torch.autograd import Variable
import torchvision.models as models
import torchvision.transforms as transforms

# Random cat img taken from Google
IMG_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg'
# Class labels used when training VGG as json, courtesy of the 'Example code' link above.
LABELS_URL = 'https://s3.amazonaws.com/outcome-blog/imagenet/labels.json'

# Let's get our class labels.
response = requests.get(LABELS_URL)  # Make an HTTP GET request and store the response.
labels = {int(key): value for key, value in response.json().items()}

# Let's get the cat img.
response = requests.get(IMG_URL)
img_stream = io.BytesIO(response.content)  # Store as byte stream.
img_b64_string = base64.encodestring(img_stream.read())  # Base64 encode img.
img_byte_string = base64.decodestring(img_b64_string)
img = Image.open(io.BytesIO(img_byte_string))  # Convert to byte stream then to pil img.

# Now that we have an img, we need to preprocess it.
# We need to:
#       * resize the img, it is pretty big (~1200x1200px).
#       * normalize it, as noted in the PyTorch pretrained models doc,
#         with, mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225].
#       * convert it to a PyTorch Tensor.
#
# We can do all this preprocessing using a transform pipeline.
min_img_size = 224  # The min size, as noted in the PyTorch pretrained models doc, is 224 px.
transform_pipeline = transforms.Compose([transforms.Resize(min_img_size),
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
vgg = models.vgg16(pretrained=True)  # This may take a few minutes.
prediction = vgg(img).data.numpy() # Returns a Tensor of shape (batch, num class labels)
index = prediction.argmax()  # Our prediction will be the index of the class label with the largest value.
print(prediction.shape, labels[index], prediction.max())  # Converts the index to a string using our labels dict
