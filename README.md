# DataFaux

[![Build Status](https://github.com/Jean-EstevezT/DataFaux/actions/workflows/ci.yml/badge.svg)](https://github.com/Jean-EstevezT/DataFaux/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Jean-EstevezT/DataFaux/blob/main/LICENSE.md)

**DataFaux** is a powerful, open-source Python tool for generating realistic and structured test data. It is designed for developers, testers, and QA engineers who need to create varied and valid datasets for testing and development without using sensitive real-world information.

Whether you need to test a data pipeline, populate a development database, or simulate user behavior, DataFaux provides a flexible and easy-to-use solution.

## Quick Start

```bash
# Install dependencies (recommended in a virtual environment)
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate # On macOS/Linux
pip install -r requirements.txt

# Generate 100 people records in CSV
python -m datafaux.main generate --preset people --count 100 --out people.csv
```

## Key Features

- **Multiple Data Generators:** Generate data for various domains, including people, e-commerce, finance, and health.
- **Multiple Export Formats:** Export data to CSV, JSON, Excel, and Parquet.
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

### CLI Usage

#### Basic Generation

Generate a CSV file with 100 records of people data:

```bash
python -m datafaux.main generate --preset people --count 100 --out people.csv
```

#### Streaming Generation

Generate a large dataset of 1,000,000 records in streaming mode to avoid memory issues. The data will be saved in chunks of 10,000 records.

```bash
python -m datafaux.main generate --preset people --count 1000000 --out large_dataset.csv --mode streaming --chunksize 10000
```

#### Testers Mode

Generate a dataset with 2% of the records containing errors. This is useful for testing data validation and cleaning pipelines.

```bash
python -m datafaux.main generate --preset ecommerce --count 1000 --out ecommerce_with_errors.csv --mode testers --error-rate 0.02
```

#### Generating from a Schema

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

#### Linking Presets

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

#### Using a `config.yaml` for Defaults

You can set default options for the CLI in a `config.yaml` file in your project directory. Any CLI argument will override the config file.

**Example `config.yaml`:**
```yaml
preset: people
count: 200
out: my_people.csv
format: csv
locale: en_US
mode: normal
```

Now you can simply run:
```bash
python -m datafaux.main generate
```
and it will use the defaults from `config.yaml`.

### Using DataFaux as a Python Library

You can use DataFaux directly from Python to generate data and export it programmatically.

#### Generate People Data

```python
from datafaux.generators import people
df = people.generate_default(count=100, seed=42, locale="en_US")
print(df.head())
```

#### Generate Ecommerce Data with Custom Customers

```python
from datafaux.generators import ecommerce
import pandas as pd
customers = pd.DataFrame([
  {"customer_id": "1", "name": "Alice", "email": "alice@example.com"},
  {"customer_id": "2", "name": "Bob", "email": "bob@example.com"}
])
df = ecommerce.generate_default(count=10, customers_df=customers)
```

#### Generate Data from a Schema

```python
import yaml
from datafaux.generators import people
with open("my_schema.yaml") as f:
  schema = yaml.safe_load(f)
df = people.generate_from_schema(schema, count=50)
```

#### Export Data to File

```python
from datafaux.utils.exporters import save_df
save_df(df, "output.csv", fmt="csv")
save_df(df, "output.parquet", fmt="parquet")
```

#### Available Generators

- `datafaux.generators.people`
- `datafaux.generators.ecommerce`
- `datafaux.generators.finance`
- `datafaux.generators.health`

Each generator provides `generate_default` and (for some) `generate_from_schema` functions.

## CLI Reference

| Option             | Description                                                                                             | Default      |
| ------------------ | ------------------------------------------------------------------------------------------------------- | ------------ |
| `--preset`         | The name of the preset to use for data generation (e.g., `people`, `ecommerce`).                        | `None`       |
| `--schema`         | The path to a YAML schema file for custom data generation.                                              | `None`       |
| `--count`, `-n`    | The number of records to generate.                                                                      | `100`        |
| `--out`, `-o`      | The name of the output file.                                                                            | `out.csv`    |
| `--format`, `-f`   | The output format (`csv`, `json`, `excel`, `parquet`).                                                  | `csv`        |
| `--seed`           | A seed for the random number generator to ensure reproducibility.                                         | `None`       |
| `--locale`         | The locale to use for data generation (e.g., `en_US`, `es_ES`).                                           | `en_US`      |
| `--mode`           | The generation mode (`normal`, `streaming`, `testers`).                                                 | `normal`     |
| `--error-rate`     | The percentage of errors to inject in `testers` mode (as a float, e.g., `0.05` for 5%).                 | `0.05`       |
| `--chunksize`      | The number of records per chunk in `streaming` mode.                                                    | `1000`       |
| `--customers-file` | *(Planned)* The path to a CSV or JSON file with customer data to be used with the `ecommerce` preset.<br>**Note:** This option is not yet implemented in the current version. | `None`       |

## Example Output

### Sample CSV Output

```csv
person_id,name,email,phone,age,registered_at
e3b0c442-98fc-1fc1-9b93-7efb171b8b6e,John Doe,john.doe@example.com,+1-555-1234,34,2023-07-15T10:23:45
f2a1c442-12ab-4bc2-8c1d-7efb171b8b6e,Jane Smith,jane.smith@example.com,+1-555-5678,28,2024-01-10T15:12:30
f9c2d442-45cd-7ef1-2b3d-7efb171b8b6e,Bob Lee,bob.lee@example.com,+1-555-9012,41,2022-11-03T08:55:12
```

### Sample JSON Output

```json
[
  {
    "person_id": "e3b0c442-98fc-1fc1-9b93-7efb171b8b6e",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-1234",
    "age": 34,
    "registered_at": "2023-07-15T10:23:45"
  },
  {
    "person_id": "f2a1c442-12ab-4bc2-8c1d-7efb171b8b6e",
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "+1-555-5678",
    "age": 28,
    "registered_at": "2024-01-10T15:12:30"
  },
  {
    "person_id": "f9c2d442-45cd-7ef1-2b3d-7efb171b8b6e",
    "name": "Bob Lee",
    "email": "bob.lee@example.com",
    "phone": "+1-555-9012",
    "age": 41,
    "registered_at": "2022-11-03T08:55:12"
  }
]
```

## Troubleshooting

- If you have dependency issues, ensure you are using a clean virtual environment and the recommended Python version (>=3.8).
- If you see import errors, check that you are running commands from the project root.
- For data generation issues, check your YAML schema format and the parameters used.

## Developer Guide

To contribute or develop DataFaux:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest
```

Follow PEP8 style and use pull requests to propose changes.

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.

## Contact

For support, suggestions, or bug reports, open an issue on GitHub or contact me through my social media.

## Changelog

- 0.1.0 (2025-08-10): First public release, data generation for people, e-commerce, finance, and health. Normal, streaming, and testers modes. Export to CSV, JSON, and Excel. YAML schema support.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.