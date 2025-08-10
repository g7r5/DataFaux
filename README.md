
# DataFaux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/jeanestevez/DataFaux/blob/main/LICENSE.md)

DataFaux is an open-source Python library and script designed to generate realistic and structured test datasets. It is the ideal tool for developers, testers, and QA teams who need to simulate data from various sectors (finance, healthcare, e-commerce, etc.) without legal risks, ensuring compliance with regulations like GDPR and HIPAA.

The main goal is to allow any developer or tester to quickly generate data with a valid structure, consistent data types, and realistic patterns, without using real personal information.

## ✨ Key Features

- **Sector-Specific Data Generation:** Create data for various domains:
  - **People:** Names, addresses, emails, etc.
  - **Finance:** Invoices, bank transactions.
  - **E-commerce:** Products, shopping carts, orders.
  - **Healthcare:** Patients, medical appointments.
- **Multiple Export Formats:**
  - CSV
  - JSON
  - Excel
- **High Customization:**
  - Define the number of records to generate.
  - Configure specific fields using presets or YAML schemas.
  - Uses [Faker](https://faker.readthedocs.io/) and custom models for greater realism.

## 🚀 Installation

To install and run DataFaux locally, follow these steps:

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/jeanestevez/DataFaux.git
    cd DataFaux
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv .venv
    ```
    ```bash
    # Activate on Windows
    .venv\Scripts\activate
    ```
    ```bash
    # Activate on macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

You can generate data using predefined presets or your own schema.

### Using a Preset

Generate a CSV with 10 records of people:
```bash
python -m datafaux.main generate --preset people --count 10 --out people.csv --format csv
```

### Using a Custom Schema

Generate a JSON file with 50 records based on a YAML schema:
```bash
python -m datafaux.main generate --schema examples/people_schema.yaml --count 50 --out people.json --format json
