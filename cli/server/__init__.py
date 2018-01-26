from flask import Flask, request
from utils.store import store


# Create App
server = Flask(__name__)


# Routes
@server.route('/apps/<app>/models/<model>/prediction', methods=['POST'])
def hello_world(app, model):
  print(request.headers.get('access-token'), store.get("access-token"), request.data)
  return ''
