from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"
reset_tokens = {}

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        token = "reset123"  # di real case ini bisa pakai uuid
        reset_tokens[token] = email
        print(f"[INFO] Link reset untuk {email}: http://127.0.0.1:5000/reset-password/{token}")
        flash("Tautan reset telah dikirim ke terminal.", "info")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if token not in reset_tokens:
        return "Token tidak valid atau kadaluarsa", 404

    if request.method == "POST":
        new_pass = request.form.get("new_password")
        confirm_pass = request.form.get("confirm_password")
        if new_pass != confirm_pass:
            flash("Kata sandi tidak cocok!", "error")
        else:
            print(f"[SUCCESS] Password untuk {reset_tokens[token]} berhasil direset!")
            del reset_tokens[token]
            flash("Kata sandi berhasil direset, silakan login.", "success")
            return redirect(url_for("login"))

    return render_template("reset_password.html", token=token)

if __name__ == "__main__":
    app.run(debug=True)
