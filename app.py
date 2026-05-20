from datetime import datetime
from flask import Flask, render_template, request, session
from crypto_core import run_cipher

app = Flask(__name__)
app.secret_key = "ganti-secret-key-ini-saat-deploy"

ALGORITHMS = {
    "caesar": "Caesar Cipher",
    "vigenere": "Vigenère Cipher",
    "affine": "Affine Cipher",
    "hill": "Hill Cipher",
    "playfair": "Playfair Cipher",
}


@app.route("/", methods=["GET", "POST"])
def index():
    result_data = None
    error = None
    selected_algorithm = request.form.get("algorithm", "caesar")
    selected_mode = request.form.get("mode", "encrypt")

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        try:
            text = request.form.get("text", "")
            result_data = run_cipher(selected_algorithm, selected_mode, text, request.form)
            history_item = {
                "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "algorithm": ALGORITHMS.get(selected_algorithm, selected_algorithm),
                "mode": "Enkripsi" if selected_mode == "encrypt" else "Dekripsi",
                "input": text[:80],
                "output": result_data["result"][:100],
            }
            history = [history_item] + session.get("history", [])
            session["history"] = history[:12]
            session.modified = True
        except Exception as exc:
            error = str(exc)

    return render_template(
        "index.html",
        algorithms=ALGORITHMS,
        result_data=result_data,
        error=error,
        history=session.get("history", []),
        selected_algorithm=selected_algorithm,
        selected_mode=selected_mode,
        form=request.form,
    )


@app.route("/clear-history", methods=["POST"])
def clear_history():
    session["history"] = []
    session.modified = True
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)
