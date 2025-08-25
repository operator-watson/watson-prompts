#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def clean_prompt(xml_text: str) -> str:
    """
    Cleans up an XML prompt string for LLM use:
    - Removes XML declaration
    - Removes namespace/schema attributes from <prompt>
    - Strips CDATA markers
    """
    # Remove XML declaration
    xml_text = re.sub(r'<\?xml.*?\?>', '', xml_text, flags=re.DOTALL)

    # Normalize <prompt ...> to just <prompt>
    xml_text = re.sub(r'<prompt[^>]*>', '<prompt>', xml_text)

    # Remove CDATA start/end markers
    xml_text = xml_text.replace('<![CDATA[', '').replace(']]>', '')

    # Trim excess whitespace
    return xml_text.strip()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file.xml>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.is_file():
        print(f"Error: {input_path} does not exist.")
        sys.exit(1)

    # Read the XML file
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_xml = f.read()

    # Clean it
    cleaned_xml = clean_prompt(raw_xml)

    # Output path
    output_path = input_path.with_name(input_path.stem + "_parsed.xml")

    # Write cleaned XML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_xml)

    print(f"Cleaned XML saved to: {output_path}")

if __name__ == "__main__":
    main()