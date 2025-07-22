from flask import Flask, request, jsonify, redirect, abort
from app.shortener import URLShortener

app = Flask(__name__)
shortener = URLShortener()

@app.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    url = data["url"]
    try:
        short_code = shortener.shorten_url(url)
    except ValueError:
        return jsonify({"error": "Invalid URL"}), 400

    short_url = request.host_url + short_code
    return jsonify({"short_code": short_code, "short_url": short_url}), 201

@app.route("/<string:short_code>", methods=["GET"])
def redirect_to_url(short_code):
    url = shortener.get_original_url(short_code)
    if not url:
        abort(404, "Short code not found")
    shortener.increment_click(short_code)
    return redirect(url)

@app.route("/api/stats/<string:short_code>", methods=["GET"])
def stats(short_code):
    stats_data = shortener.get_stats(short_code)
    if not stats_data:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify(stats_data)
