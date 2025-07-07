from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import tempfile
import logging
import io
from utils.background import remove_bg_add_new
from utils.enhance import enhance_image

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Limit upload size to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def parse_color(color_str):
    # Accepts "255,255,255" or "#ffffff" or "#ffffffff"
    if not color_str:
        return None
    color_str = color_str.strip()
    if color_str.startswith("#"):
        color_str = color_str.lstrip("#")
        if len(color_str) == 6:
            r, g, b = tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
            return (r, g, b, 255)
        elif len(color_str) == 8:
            r, g, b, a = tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4, 6))
            return (r, g, b, a)
        else:
            return None
    elif "," in color_str:
        try:
            parts = [int(x) for x in color_str.split(",")]
            if len(parts) == 3:
                return tuple(parts) + (255,)
            elif len(parts) == 4:
                return tuple(parts)
        except Exception:
            return None
    return None

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File is too large. Max size is 10MB."}), 413

@app.route("/remove-bg", methods=["POST"])
def remove_background():
    try:
        file = request.files.get("file")
        bg_color_str = request.form.get("bg_color")  # Optional
        bg_image = request.files.get("bg_image")  # Optional

        if not file or not file.filename:
            return jsonify({"error": "No image uploaded"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type"}), 400

        bg_color = parse_color(bg_color_str) if bg_color_str else None

        with tempfile.TemporaryDirectory() as tmpdir:
            input_filename = file.filename if file.filename else "input.jpg"
            input_path = os.path.join(tmpdir, input_filename)
            file.save(input_path)

            output_path = os.path.join(tmpdir, "output.png")
            bg_image_path = None

            if bg_image and bg_image.filename:
                if not allowed_file(bg_image.filename):
                    return jsonify({"error": "Unsupported background image type"}), 400
                bg_image_path = os.path.join(tmpdir, "bg.jpg")
                bg_image.save(bg_image_path)

            try:
                remove_bg_add_new(input_path, output_path, bg_color, bg_image_path)
            except Exception as e:
                logger.error(f"remove_bg_add_new failed: {e}")
                return jsonify({"error": "Background removal failed: " + str(e)}), 500

            with open(output_path, "rb") as f:
                data = f.read()
            return send_file(
                io.BytesIO(data),
                mimetype="image/png",
                as_attachment=True,
                download_name="no_bg.png"
            )
    except Exception as e:
        logger.error(f"Request failed with status code 500: {e}")
        return jsonify({"error": "Request failed with status code 500: " + str(e)}), 500

@app.route("/enhance", methods=["POST"])
def enhance():
    try:
        file = request.files.get("file")
        if not file or not file.filename:
            return jsonify({"error": "No image uploaded"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type"}), 400

        with tempfile.TemporaryDirectory() as tmpdir:
            input_filename = file.filename if file.filename else "input.jpg"
            input_path = os.path.join(tmpdir, input_filename)
            output_path = os.path.join(tmpdir, "enhanced.jpg")
            file.save(input_path)

            try:
                enhance_image(input_path, output_path)
            except Exception as e:
                logger.error(f"enhance_image failed: {e}")
                return jsonify({"error": "Enhancement failed: " + str(e)}), 500

            return send_file(output_path, download_name="enhanced.jpg", mimetype="image/jpeg")
    except Exception as e:
        logger.error(f"Request failed with status code 500: {e}")
        return jsonify({"error": "Request failed with status code 500: " + str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
