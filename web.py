from flask import request, jsonify
from presidio import analyze


def detect_pii(text: str):
    results = analyze(text)

    return [
        {
            "start": r.start,
            "end": r.end,
            "entity": r.entity_type,
            "score": round(r.score, 3),
            "match": text[r.start : r.end],
        }
        for r in results
    ]


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
