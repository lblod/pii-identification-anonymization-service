from flask import request, jsonify
from presidio import detect_pii
from bpmn import process_bpmn_file


@app.route("/raw", methods=["POST"])
def detect_raw():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")
    output = detect_pii(text)
    return jsonify(output)

@app.route("/bpmn", methods=["POST"])
def detect_bpmn():
    try:
        file = request.files.get('file')
        output = process_bpmn_file(file)
        return jsonify(output)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500