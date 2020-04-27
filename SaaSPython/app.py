from flask import Flask, render_template, request
import io
import os
import json

# Imports the Google Cloud client library
from google.cloud.vision import types
from google.cloud import vision
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('uploadImage.html')

@app.route('/detectedLabels',methods=('GET','POST'))
def callToVisionApi():
   client = vision.ImageAnnotatorClient()
   # Recieves the image data and convert the image into bytearray
   content = request.files['image'].read()

   image = types.Image(content=content)

   # Performs label detection on the image file
   response = client.label_detection(image=image)
   labels = response.label_annotations

   posts = []
   for label in labels:
      data = {}
      data['mid'] = label.mid
      data['description'] = label.description
      data['score'] = label.score
      data['topicality'] = label.topicality
      posts.append(data)

   return render_template('output.html', posts =posts)

if __name__ == '__main__':
   app.run()