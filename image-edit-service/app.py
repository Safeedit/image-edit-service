from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import tempfile
from utils.background import remove_bg_add_new  # ✅ Only this is needed now

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def health():
    return jsonify({"message": "✅ BG Removal Service is live!"})

@app.route("/remove-bg", methods=["POST"])
def remove_background():
    try:
        file = request.files.get("file")
        bg_color = request.form.get("bg_color")
        bg_image = request.files.get("bg_image")

        if not file:
            return jsonify({"error": "No image uploaded"}), 400

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, file.filename)
            file.save(input_path)

            output_path = os.path.join(tmpdir, "output.png")
            bg_image_path = None

            if bg_image:
                bg_image_path = os.path.join(tmpdir, "bg.jpg")
                bg_image.save(bg_image_path)

            remove_bg_add_new(input_path, output_path, bg_color, bg_image_path)

            return send_file(output_path, mimetype="image/png", download_name="no_bg.png")
    except Exception as e:
        print("🔥 Error in /remove-bg:", str(e))
        return jsonify({"error": f"BG removal failed: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
