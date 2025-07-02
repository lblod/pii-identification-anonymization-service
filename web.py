from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from presidio import detect_pii

def extract_text_from_bpmn(bpmn_content) -> list:
    try:
        root = ET.fromstring(bpmn_content)
        unique_texts = set()
        
        for elem in root.iter():
            if 'name' in elem.attrib:
                name_value = elem.attrib['name'].strip()
                unique_texts.add(name_value)
        
        return list(unique_texts)
    
    except ET.ParseError as e:
        raise ValueError(f"Invalid BPMN XML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing BPMN file: {str(e)}")

def process_bpmn_file(file):
    if not file or file.filename == '':
        raise ValueError("No file selected")
    
    file_content = file.read()
    if not file_content:
        raise ValueError("Empty file")
    
    if isinstance(file_content, bytes):
        file_content = file_content.decode('utf-8')
    
    extracted_texts = extract_text_from_bpmn(file_content)
    combined_text = " ".join(extracted_texts)
    pii_results = detect_pii(combined_text)
    
    return {
        "extracted_texts": extracted_texts,
        "pii_results": pii_results,
        "total_pii_found": len(pii_results)
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
        file = request.files.get('file')
        output = process_bpmn_file(file)
        return jsonify(output)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500