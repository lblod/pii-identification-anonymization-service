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


def analyze(text):
    try:
        results = analyzer.analyze(text=text, language="nl")
    except ValueError:
        results = analyzer.analyze(text=text, language="en")

    return results
