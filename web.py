from flask import request, jsonify
from presidio import detect_pii
from bpmn import extract_elem_from_bpmn


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


@app.route("/raw", methods=["POST"])
def detect_raw():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")
    output = detect_pii(text)
    return jsonify(output)


@app.route("/bpmn", methods=["POST"])
def detect_bpmn():
    try:
        file = request.files.get("file")
        output = process_bpmn_file(file)
        return jsonify(output)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
