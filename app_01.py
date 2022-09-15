from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
#import os
from PIL import Image
#import sys
#import time

import json

with open('secret.json') as f:
    secret = json.load(f)

KEY = secret['KEY']
ENDPOINT = secret['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    local_image = open(filepath, "rb")

    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
        
    return tags_name

def detect_objects(filepath):
    local_image = open(filepath, "rb")

    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects

import streamlit as st
from PIL import ImageDraw # imageを読み込む
from PIL import ImageFont # フォントを修正する


st.title('物体検出アプリ')

uploaded_file = st.file_uploader('Choose an image...', type=['jpg','png'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'   #image
    img.save(img_path)
    objects = detect_objects(img_path)

    # 描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font='./Helvetica 400.ttf', size=50) # フォント取得 
        text_w, text_h = draw.textsize(caption, font=font)             # テキストサイズを取得

        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='green', width=5) # 写真の枠組みを指定
        draw.rectangle([(x, y), (x+text_w, y+text_h)], fill='green')   # 文字の枠組み指定
        draw.text((x, y), caption, fill='white', font=font)            # 文字の記載

    st.image(img)

    tags_name = get_tags(img_path)   #  ’〇〇’で分かれている。
    tags_name = ', '.join(tags_name) # , で結合する
    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'> {tags_name}')    