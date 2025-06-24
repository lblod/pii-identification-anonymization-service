from flask import request, jsonify
from presidio import detect_pii


@app.route("/raw", methods=["POST"])
def detect_raw():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")
    output = detect_pii(text)
    return jsonify(output), 200


@app.route("/bpmn", methods=["POST"])
def detect_bpmn():
    # TODO: implement BPMN traversal + multiple detect_pii calls
    return jsonify({"message": "Not implemented yet"}), 501
