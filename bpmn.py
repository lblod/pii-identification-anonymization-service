import xml.etree.ElementTree as ET

def extract_elem_from_bpmn(bpmn_content) -> list:
    elements = []
    root = ET.fromstring(bpmn_content)
    try:
        for elem in root.iter():
            if 'name' in elem.attrib:
                elements.append({
                    "id": elem.attrib.get("id", ""),
                    "name": elem.attrib['name'].strip(),
                })
        return list(elements)
    
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
    
    extracted_elements = extract_elem_from_bpmn(file_content)
    pii_results = []
    for elem in extracted_elements:
        pii_result = detect_pii(elem['name'])
        for key in pii_result:
            key['id'] = elem['id']
            pii_results.append(key)
    
    return {
        "extracted_elements": extracted_elements,
        "pii_results": pii_results,
        "total_pii_found": len(pii_results)
    }