from flask import request, jsonify, Response
from identification import detect_pii
from anonymization import mask_spans
from bpmn import (
    deserialize_bpmn,
    serialize_bpmn,
    extract_elem_from_bpmn,
    get_element_name,
    set_element_name,
)
import json


########################################################################
# RAW
########################################################################


@app.route("/raw/identify", methods=["POST"])
def identify_raw():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")

    if not isinstance(text, str):
        return jsonify({"error": "Invalid payload"}), 400

    output = detect_pii(text)
    return jsonify(output)


@app.route("/raw/anonymize", methods=["POST"])
def anonymize_raw():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")
    spans = data.get("spans", [])

    if not isinstance(text, str) or not isinstance(spans, list):
        return jsonify({"error": "Invalid payload"}), 400

    result = mask_spans(text, spans)
    return jsonify({"anonymized_text": result}), 200


########################################################################
# BPMN
########################################################################


def process_bpmn_file(file):
    if not file or file.filename == "":
        raise ValueError("No file selected")

    file_content = file.read()
    if not file_content:
        raise ValueError("Empty file")

    if isinstance(file_content, bytes):
        file_content = file_content.decode("utf-8")

    extracted_elements = extract_elem_from_bpmn(file_content)
    pii_results = []
    for elem in extracted_elements:
        pii_result = detect_pii(elem["name"])
        for key in pii_result:
            key["id"] = elem["id"]
            pii_results.append(key)

    return {
        "extracted_elements": extracted_elements,
        "pii_results": pii_results,
        "total_pii_found": len(pii_results),
    }


@app.route("/bpmn/identify", methods=["POST"])
def identify_bpmn():
    try:
        file = request.files.get("file")
        output = process_bpmn_file(file)
        return jsonify(output)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/bpmn/anonymize", methods=["POST"])
def anonymize_bpmn():
    file = request.files.get("file")

    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    bpmn = deserialize_bpmn(file)

    pointers = request.form.get("pointers", "[]")
    pointers = json.loads(pointers)

    if not isinstance(pointers, list):
        return jsonify({"error": "Invalid payload"}), 400

    groups = {}
    for p in pointers:
        groups.setdefault(p["id"], []).append(p)

    for element_id, spans in groups.items():
        original = get_element_name(bpmn, element_id)
        masked = mask_spans(original, spans)
        set_element_name(bpmn, element_id, masked)

    return Response(serialize_bpmn(bpmn), mimetype="application/xml"), 200
