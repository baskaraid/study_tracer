from flask import Flask, render_template, redirect, url_for, session
from controllers.auth_controller import auth_bp
from controllers.kuesioner_controller import kuesioner_bp
from controllers.stakeholder_controller import stakeholder_bp

app = Flask(__name__)
app.secret_key = "rahasia_super_aman"

# Register Blueprint
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(kuesioner_bp, url_prefix="/kuesioner")
app.register_blueprint(stakeholder_bp, url_prefix="/stakeholder")

@app.route("/")
def home():
    # halaman utama langsung ke form kuesioner tanpa login
    return redirect(url_for("kuesioner.tracer_menu"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ✅ untuk server WSGI (PythonAnywhere)
application = app

# ✅ tetap bisa jalan di lokal
if __name__ == "__main__":
    app.run(debug=True)
