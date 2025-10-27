from flask import Blueprint, render_template, request, redirect, url_for, current_app
import os
import yaml
from ml_development import run_detection  # pastikan ini sudah versi baru

post_bp = Blueprint("post_routers", __name__, url_prefix="/")

@post_bp.route("/deteksi", methods=["GET", "POST"])
def deteksi():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            # Folder upload & hasil
            upload_dir = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
            os.makedirs(upload_dir, exist_ok=True)

            # Simpan file upload
            upload_path = os.path.join(upload_dir, file.filename)
            file.save(upload_path)

            # Jalankan model
            model_path = current_app.config.get("MODEL_PATH", "model/best.onnx")
            label_path = current_app.config.get("LABEL_PATH", "model/label.yaml")
            # baca semua label dari YAML
            with open(label_path, 'r', encoding='utf-8') as f:
                labels_yaml = yaml.safe_load(f)['names']
            _, scores, class_labels = run_detection(model_path, label_path, upload_path)

            # Hitung hasil prediksi
            class_count = len(class_labels)
            result_image = url_for('static', filename=f"uploads/{file.filename}")

            return render_template(
                "hasil_deteksi.html",
                image_url=result_image,
                class_count=class_count,
                class_labels=class_labels,  # gunakan class_labels
                scores=scores,
                yaml_labels=labels_yaml
            )

    return render_template("deteksi.html")


@post_bp.route("/simpan-edit", methods=["POST"])
def simpan_edit():
    image_path = request.form.get("image_path")
    semua_benar = request.form.get("semua_benar")

    # Ambil semua class_label dan counter
    class_labels = []
    counters = []
    i = 1
    while True:
        label = request.form.get(f"class_label_{i}")
        counter = request.form.get(f"counter_{i}")
        if label is None:
            break
        class_labels.append(label)
        counters.append(int(counter))
        i += 1

    if semua_benar:
        print("✅ Semua hasil deteksi dianggap benar.")
    else:
        print("🔧 Label hasil edit:")
        for idx, (lbl, cnt) in enumerate(zip(class_labels, counters), 1):
            print(f"Objek {idx}: class_label={lbl}, counter={cnt}")

    print(f"🖼️ Gambar: {image_path}")
    return redirect(url_for("post_routers.deteksi"))
