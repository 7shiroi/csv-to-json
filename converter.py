import csv
import json
import os
import argparse
from typing import Dict, Any

def detect_type(value: str) -> Any:
    value = value.strip()
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def csv_to_json(csv_file: str, minify: bool = False, array_prefix: str = "JA_", array_separator: str = ",") -> Dict[str, Any]:
    result = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_key = detect_type(row[reader.fieldnames[0]])
            entry = {}
            for key, value in row.items():
                if key != reader.fieldnames[0] and value.strip():  # Skip empty values
                    if key.startswith(array_prefix):
                        array_values = [detect_type(v.strip()) for v in value.split(array_separator) if v.strip()]
                        if array_values:  # Only add non-empty arrays
                            entry[key[len(array_prefix):]] = array_values
                    else:
                        entry[key] = detect_type(value)
            result[id_key] = entry
    
    return result

def process_file(input_file: str, output_file: str, minify: bool, array_prefix: str, array_separator: str):
    json_data = csv_to_json(input_file, minify, array_prefix, array_separator)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=None if minify else 2, ensure_ascii=False)
    print(f"Converted {input_file} to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert CSV to JSON")
    parser.add_argument("input", help="Input CSV file or directory")
    parser.add_argument("--output", "-o", default=None, help="Output file or directory location (default: same as input)")
    parser.add_argument("--minify", action="store_true", help="Minify JSON output")
    parser.add_argument("--array-prefix", default="JA_", help="Prefix for array columns (default: JA_)")
    parser.add_argument("--array-separator", default=",", help="Separator for array values (default: ,)")
    args = parser.parse_args()

    if os.path.isfile(args.input):
        if args.output:
            if os.path.isdir(args.output):
                output_file = os.path.join(args.output, os.path.splitext(os.path.basename(args.input))[0] + ".json")
            else:
                output_file = args.output
        else:
            output_file = os.path.splitext(args.input)[0] + ".json"
        process_file(args.input, output_file, args.minify, args.array_prefix, args.array_separator)
    elif os.path.isdir(args.input):
        if args.output:
            output_dir = args.output if args.output != '.' else os.getcwd()
        else:
            output_dir = os.path.join(args.input, "jsons")
        os.makedirs(output_dir, exist_ok=True)
        for file in os.listdir(args.input):
            if file.endswith(".csv"):
                input_file = os.path.join(args.input, file)
                output_file = os.path.join(output_dir, os.path.splitext(file)[0] + ".json")
                process_file(input_file, output_file, args.minify, args.array_prefix, args.array_separator)
    else:
        print("Invalid input. Please provide a CSV file or directory.")

if __name__ == "__main__":
    main()
