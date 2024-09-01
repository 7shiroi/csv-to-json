# CSV to JSON Converter

This project provides a Python script that converts CSV files to JSON format with various customization options.

## Features

- Convert single CSV files or entire directories of CSV files to JSON
- Detect and convert data types automatically (boolean, integer, float, string)
- Support for array columns with customizable prefix and separator
- Option to minify JSON output
- Customizable output location

## Requirements

- Python 3.6+

## Usage

```bash
python converter.py [-h] [--output OUTPUT] [--minify] [--array-prefix ARRAY_PREFIX] [--array-separator ARRAY_SEPARATOR] input
```

### Arguments

- `input`: Path to the input CSV file or directory containing CSV files
- `--output OUTPUT`: Optional output file or directory location
- `--minify`: Minify the JSON output
- `--array-prefix ARRAY_PREFIX`: Prefix for array columns (default: `JA_`)
- `--array-separator ARRAY_SEPARATOR`: Separator for array values (default: `,`)

## Example

Convert a single CSV file to JSON:

```bash
python converter.py --output output.json --minify --array-prefix JA_ --array-separator , input.csv
```

Convert all CSV files in a directory to JSON:

```bash
python converter.py input_directory --output output_directory --array-prefix "ARRAY_" --array-separator "|"
```

## How it works

The script reads CSV files, automatically detects data types, and converts them to appropriate JSON types. It also handles array columns, which are identified by a customizable prefix (default: "JA\_"). The values in these columns are split using a specified separator (default: ",") and converted into JSON arrays.

For more details on the implementation, see the `converter.py` file:

## License

[MIT License](LICENSE)
