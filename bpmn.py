import xml.etree.ElementTree as ET


def extract_elem_from_bpmn(bpmn_content) -> list:
    elements = []
    root = ET.fromstring(bpmn_content)
    try:
        for elem in root.iter():
            if "name" in elem.attrib:
                elements.append(
                    {
                        "id": elem.attrib.get("id", ""),
                        "name": elem.attrib["name"].strip(),
                    }
                )
        return list(elements)

    except ET.ParseError as e:
        raise ValueError(f"Invalid BPMN XML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing BPMN file: {str(e)}")
