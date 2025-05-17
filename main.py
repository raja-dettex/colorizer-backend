from flask import Flask, request, jsonify
import os

app = Flask(__name__)
upload_folder = os.path.join(os.path.abspath(os.curdir), 'DeOldify', 'uploads')
allowed_extensions = ['jpg', 'jpeg', 'png']

def allowed(file: str):
    return '.' in file and file.rsplit('.')[1].lower() in allowed_extensions

os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route("/hello")
def hello_world():
    print("here")
    return "Hello, World!"

@app.route("/upload", methods=['POST'])
def upload_file():
    print("requst got")
    if 'file' not in request.files:
        return jsonify({'error' : 'no file part in request'}), 400
    file = request.files['file']
    print(file.filename)
    if file.filename == '':
        return jsonify({'error' : 'no filename'}), 400
    if file and allowed(file.filename):
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        return jsonify({
            'message' : "file uploaded succesfully",
            'filename' : file.filename,
            'path' : path
        })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)
