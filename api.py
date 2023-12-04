from flask import Flask, request, jsonify
from PIL import Image
import pillow_heif 

# Register HEIF
pillow_heif.register_heif_opener()

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': "No image part"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': "No selected file"}), 400
    if file and allowed_file(file.filename):
        try:
            image = Image.open(file.stream)
            image = image.convert('RGB')

            image.save('uploads/image.jpg', 'JPEG')

            return jsonify({'message': "Image Uploded successfully"})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': "Invalid file format"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'heic'


if __name__ == '__main__':
    app.run(debug=True)