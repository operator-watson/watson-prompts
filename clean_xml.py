#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def clean_prompt(xml_text: str) -> str:
    """
    Cleans XML:
    - Removes XML declaration
    - Removes namespace/schema attributes from <prompt>
    - Strips CDATA while preserving internal indentation
    - Avoids extra spaces on closing tags
    """
    xml_text = re.sub(r'<\?xml.*?\?>', '', xml_text, flags=re.DOTALL)
    xml_text = re.sub(r'<prompt[^>]*>', '<prompt>', xml_text)
    xml_text = re.sub(
        r'<!\[CDATA\[\s*(.*?)\s*\]\]>',
        lambda m: m.group(1),
        xml_text,
        flags=re.DOTALL
    )
    return xml_text.strip()

def process_file(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_xml = f.read()
    cleaned_xml = clean_prompt(raw_xml)
    output_path = file_path.with_name(file_path.stem + "_parsed.xml")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_xml)
    print(f"Cleaned XML saved to: {output_path}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file_or_folder>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if path.is_file():
        process_file(path)
    elif path.is_dir():
        xml_files = list(path.rglob("*.xml"))
        if not xml_files:
            print("No XML files found in the folder.")
            sys.exit(1)
        for xml_file in xml_files:
            process_file(xml_file)
    else:
        print(f"Error: {path} does not exist.")
        sys.exit(1)

if __name__ == "__main__":
    main()