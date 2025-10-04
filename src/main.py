import random
import string
from flask import Flask, render_template, redirect, request

import db_connector

app = Flask(__name__)


def get_short_code() -> str:
    short_code = "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=6
        )
    )
    return short_code


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        original_url = request.form["original-url"]
        short_code = get_short_code()
        db_connector.add_url(original_url, short_code)
        shortened_url = f"{request.host_url}{short_code}"
        return render_template("index.html", shortened_url=shortened_url)
    else:
        return render_template("index.html")


@app.route("/<short_code>")
def shortened_url(short_code: str = None):
    original_url = db_connector.get_url(short_code)
    if original_url:
        return redirect(original_url)

    return "Page not found", 404


if __name__ == "__main__":
    app.run(debug=True)
