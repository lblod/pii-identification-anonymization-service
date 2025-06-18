from flask import request, jsonify
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

@app.route("/test", methods=["POST"])
def detect_pii():
    """
    Expect JSON: { "text": "<your text here>" }
    Returns: list of PII spans with start/end/entity/score/match
    """
    
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")
    
    results = analyzer.analyze(text=text, language="en")

    output = []
    for res in results:
        output.append({
            "start": res.start,
            "end": res.end,
            "entity": res.entity_type,
            "score": round(res.score, 3),
            "match": text[res.start:res.end]
        })

    return jsonify(output), 200
