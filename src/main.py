import os
import random
import string
from dotenv import load_dotenv
import requests
from flask import Flask, render_template, redirect, request
from apscheduler.schedulers.background import BackgroundScheduler

import db_connector

load_dotenv()

app = Flask(__name__)
server_name = os.environ.get("HOST_URL")


def keep_awake():
    requests.request(method="GET", url=server_name)


scheduler = BackgroundScheduler()
scheduler.add_job(func=keep_awake, trigger="interval", minutes=1)
scheduler.add_job(func=db_connector.delete_expired_urls, trigger="interval", hours=1)
scheduler.start()


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
        validity_period_str = request.form["validity-period"]

        match (validity_period_str):
            case "1 D":
                validity_days = 1
            case "10 D":
                validity_days = 10
            case "1 M":
                validity_days = 30
            case "6 M":
                validity_days = 182
            case "12 M":
                validity_days = 365
            case _:
                validity_days = 1

        short_code = get_short_code()
        db_connector.add_url(original_url, short_code, validity_days)
        shortened_url = f"{request.host_url}{short_code}"
        return render_template("index.html", shortened_url=shortened_url)
    else:
        return render_template("index.html")


@app.route("/<short_code>")
def shortened_url(short_code: str = None):
    original_url = db_connector.get_url(short_code)
    if original_url:
        db_connector.increment_clicks(short_code)
        return redirect(original_url)

    return "Page not found", 404


if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        scheduler.shutdown()
