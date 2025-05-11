from flask import Flask, request, jsonify
from google.cloud import vision
import io
import os

app = Flask(__name__)

# 设置 Google Cloud 凭据（实际部署时通过环境变量注入）
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account.json'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    content = file.read()
    
    # 调用 Google Vision API
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return jsonify({"text": texts[0].description if texts else "No text found."})

# Vercel 适配器
def vercel_handler(request):
    from flask import Request
    flask_request = Request.from_values(
        path=request.path,
        method=request.method,
        headers=request.headers,
        data=request.body
    )
    with app.request_context(flask_request.environ):
        return app.full_dispatch_request()