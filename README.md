# DataFaux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/jeanestevez/DataFaux/blob/main/LICENSE.md)

**DataFaux** is a powerful, open-source Python tool for generating realistic and structured test data. It is designed for developers, testers, and QA engineers who need to create varied and valid datasets for testing and development without using sensitive real-world information.

Whether you need to test a data pipeline, populate a development database, or simulate user behavior, DataFaux provides a flexible and easy-to-use solution.

## Key Features

- **Multiple Data Generators:** Generate data for various domains, including people, e-commerce, finance, and health.
- **Multiple Export Formats:** Export data to CSV, JSON, and Excel.
- **Streaming Mode:** Generate large datasets without running out of memory by processing data in chunks.
- **Testers Mode:** Intentionally inject errors (e.g., null values, wrong data types) into your data to test the robustness of your data processing systems.
- **Schema-Driven Generation:** Define complex data structures using YAML schemas for highly customized data generation.
- **Relational Presets:** Generate related data, such as e-commerce orders linked to a specific set of customers.
- **Extensible:** Easily add new data generators and presets.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jeanestevez/DataFaux.git
    cd DataFaux
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv .venv

    # Activate on Windows
    .venv\Scripts\activate

    # Activate on macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Basic Generation

Generate a CSV file with 100 records of people data:

```bash
python -m datafaux.main generate --preset people --count 100 --out people.csv
```

### Streaming Generation

Generate a large dataset of 1,000,000 records in streaming mode to avoid memory issues. The data will be saved in chunks of 10,000 records.

```bash
python -m datafaux.main generate --preset people --count 1000000 --out large_dataset.csv --mode streaming --chunksize 10000
```

### Testers Mode

Generate a dataset with 2% of the records containing errors. This is useful for testing data validation and cleaning pipelines.

```bash
python -m datafaux.main generate --preset ecommerce --count 1000 --out ecommerce_with_errors.csv --mode testers --error-rate 0.02
```

### Generating from a Schema

Define your own data structure in a YAML file (e.g., `my_schema.yaml`) and use it to generate data.

**`my_schema.yaml`:**
```yaml
type: people
fields:
  - name: full_name
    provider: name
  - name: job_title
    provider: job
  - name: credit_card
    provider: credit_card_number
```

**Command:**
```bash
python -m datafaux.main generate --schema my_schema.yaml --count 50 --out custom_data.json --format json
```

### Linking Presets

Generate e-commerce orders for a specific set of customers from a file.

**`customers.csv`:**
```csv
customer_id,name,email
1,John Doe,john.doe@example.com
2,Jane Smith,jane.smith@example.com
```

**Command:**
```bash
python -m datafaux.main generate --preset ecommerce --customers-file customers.csv --count 100 --out orders.csv
```

## CLI Reference

| Option             | Description                                                                                             | Default      |
| ------------------ | ------------------------------------------------------------------------------------------------------- | ------------ |
| `--preset`         | The name of the preset to use for data generation (e.g., `people`, `ecommerce`).                        | `None`       |
| `--schema`         | The path to a YAML schema file for custom data generation.                                              | `None`       |
| `--count`, `-n`    | The number of records to generate.                                                                      | `100`        |
| `--out`, `-o`      | The name of the output file.                                                                            | `out.csv`    |
| `--format`, `-f`   | The output format (`csv`, `json`, `excel`).                                                             | `csv`        |
| `--seed`           | A seed for the random number generator to ensure reproducibility.                                         | `None`       |
| `--locale`         | The locale to use for data generation (e.g., `en_US`, `es_ES`).                                           | `en_US`      |
| `--mode`           | The generation mode (`normal`, `streaming`, `testers`).                                                 | `normal`     |
| `--error-rate`     | The percentage of errors to inject in `testers` mode (as a float, e.g., `0.05` for 5%).                 | `0.05`       |
| `--chunksize`      | The number of records per chunk in `streaming` mode.                                                    | `1000`       |
| `--customers-file` | The path to a CSV or JSON file with customer data to be used with the `ecommerce` preset.             | `None`       |

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
