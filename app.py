import os
from flask import Flask, render_template, request, send_from_directory
import trimesh

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    part = request.form.get("part")
    tolerance = float(request.form.get("tolerance"))
    scale = float(request.form.get("scale"))

    # Create a simple cube mesh as placeholder for the part
    mesh = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
    mesh.apply_scale(scale / 10.0)

    # Apply tolerance by shrinking or expanding
    mesh.apply_scale(1.0 + tolerance)

    filename = f"{part}.stl"
    filepath = os.path.join("models", filename)
    mesh.export(filepath)

    return send_from_directory("models", filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
