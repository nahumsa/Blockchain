from Blockchain import Blockchain
from flask import Flask, request
import requests

# Initializing flask application
app = Flask(__name__)

# Initializing Blockchain object
blockchain = Blockchain()
