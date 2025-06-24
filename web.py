from flask import request, jsonify
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

nlp_configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "nl", "model_name": "nl_core_news_md"},
        {"lang_code": "en", "model_name": "en_core_web_md"},
    ],
}

provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
nlp_engine = provider.create_engine()

analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine,
    supported_languages=["nl", "en"],
)


def detect_pii(text: str):
    try:
        results = analyzer.analyze(text=text, language="nl")
    except ValueError:
        results = analyzer.analyze(text=text, language="en")

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
