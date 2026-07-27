import os
import io
import json
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pixelhue import extract_palette

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extract', methods=['POST'])
def extract_colors():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image provided'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use PNG, JPG, GIF, or WebP.'}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)

    try:
        num_colors = request.form.get('num_colors', type=int, default=6)
        if num_colors is None:
            num_colors = 6
        num_colors = max(3, min(10, num_colors))
        palette = extract_palette(upload_path, num_colors=num_colors)
        return jsonify({'palette': palette})
    except Exception as e:
        print(f"Error extracting palette: {e}")
        return jsonify({'error': 'Could not extract palette from the image.'}), 500
    finally:
        if os.path.exists(upload_path):
            os.remove(upload_path)


@app.route('/download', methods=['POST'])
def download_palette():
    data = request.get_json()
    if not data or 'palette' not in data:
        return jsonify({'error': 'No palette data provided'}), 400

    palette = data['palette']
    fmt = data.get('format', 'txt')

    if fmt == 'json':
        content = json.dumps(palette, indent=2)
        filename = 'palette.json'
        mimetype = 'application/json'
    elif fmt == 'css':
        lines = [f"  --color-{i+1}: {c['hex']};" for i, c in enumerate(palette)]
        content = ":root {\n" + "\n".join(lines) + "\n}"
        filename = 'palette.css'
        mimetype = 'text/css'
    else:
        lines = []
        for i, c in enumerate(palette):
            lines.append(f"Color {i+1}: {c['hex']}  RGB{c['rgb']}  {round(c['percentage'] * 100)}%")
        content = "\n".join(lines)
        filename = 'palette.txt'
        mimetype = 'text/plain'

    return send_file(
        io.BytesIO(content.encode()),
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
