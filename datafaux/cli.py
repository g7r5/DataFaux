import click
import sys
import yaml
import os
from .config import DEFAULT_ROWS, DEFAULT_LOCALE, SUPPORTED_FORMATS, PRESETS, CHUNKSIZE_DEFAULT
from .generators import people as people_gen
from .generators import ecommerce as ecommerce_gen
from .utils.exporters import save_df, save_df_stream
from .utils.validators import validate_schema

@click.group()
def main():
    """DataFaux — Test Data Set Generator"""
    pass

@main.command()
@click.option("--preset", type=click.Choice(PRESETS), help="Quick template (preset).")
@click.option("--schema", type=click.Path(exists=True), help="YAML/JSON schema for data generation.")
@click.option("--count", "-n", default=DEFAULT_ROWS, help="Number of records to generate.")
@click.option("--out", "-o", default="out.csv", help="Output file.")
@click.option("--format", "-f", "fmt", default="csv", type=click.Choice(SUPPORTED_FORMATS), help="Output format.")
@click.option("--seed", default=None, type=int, help="Seed for reproducibility.")
@click.option("--locale", default=DEFAULT_LOCALE, help="Locale for Faker (e.g., en_US, es_ES).")
@click.option("--mode", type=click.Choice(["normal", "streaming", "testers"]), default="normal",
              help="Generation mode: normal (in-memory), streaming (by chunks), testers (injects errors)")
@click.option("--error-rate", default=0.05, help="Percentage of errors to inject in testers mode")
@click.option("--chunksize", default=CHUNKSIZE_DEFAULT, help="Chunksize for streaming")
@click.option("--customers-file", type=click.Path(exists=True), default=None, help="CSV or JSON file with customer data for ecommerce preset.")
@click.option("--verbose", is_flag=True, default=False, help="Enable verbose logging output.")
def generate(preset, schema, count, out, fmt, seed, locale, mode, error_rate, chunksize, customers_file, verbose):
    """Generate dataset with preset or schema. Supports config.yaml for default options."""
    # Load config.yaml if present
    config = {}
    config_path = os.path.join(os.getcwd(), "config.yaml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            if verbose:
                click.echo(f"[Verbose] Loaded config.yaml: {config}")
        except Exception as e:
            click.secho(f"[Warning] Could not load config.yaml: {e}", fg="yellow")

    # Use config values as defaults if CLI args are not set (None or default)
    preset = preset or config.get("preset")
    schema = schema or config.get("schema")
    count = count if count != DEFAULT_ROWS else config.get("count", count)
    out = out if out != "out.csv" else config.get("out", out)
    fmt = fmt if fmt != "csv" else config.get("format", fmt)
    seed = seed if seed is not None else config.get("seed")
    locale = locale if locale != DEFAULT_LOCALE else config.get("locale", locale)
    mode = mode if mode != "normal" else config.get("mode", mode)
    error_rate = error_rate if error_rate != 0.05 else config.get("error_rate", error_rate)
    chunksize = chunksize if chunksize != CHUNKSIZE_DEFAULT else config.get("chunksize", chunksize)
    customers_file = customers_file or config.get("customers_file")

    if verbose:
        click.echo(f"[Verbose] Options: preset={preset}, schema={schema}, count={count}, out={out}, format={fmt}, seed={seed}, locale={locale}, mode={mode}, error_rate={error_rate}, chunksize={chunksize}, customers_file={customers_file}")

    if not preset and not schema:
        click.secho("[Error] You must specify either --preset or --schema (in CLI or config.yaml).", fg="red")
        click.secho("Tip: Use --preset people or --schema my_schema.yaml", fg="yellow")
        sys.exit(1)

    df = None

    if schema:
        try:
            with open(schema, "r", encoding="utf-8") as f:
                doc = yaml.safe_load(f)
            if verbose:
                click.echo(f"[Verbose] Loaded schema: {doc}")
        except Exception as e:
            click.secho(f"[Error] Failed to load schema file: {e}", fg="red")
            click.secho("Tip: Check that the file exists and is valid YAML.", fg="yellow")
            sys.exit(1)
        ok, msg = validate_schema(doc)
        if not ok:
            click.secho(f"[Error] Invalid schema: {msg}", fg="red")
            click.secho("Tip: Your schema YAML must include a 'type' and a list of 'fields'.", fg="yellow")
            sys.exit(1)
        stype = doc.get("type")
        if verbose:
            click.echo(f"[Verbose] Schema type: {stype}")
        if stype == "people":
            df = people_gen.generate_from_schema(doc, count=count, seed=seed, locale=locale)
        elif stype == "ecommerce":
            df = ecommerce_gen.generate_from_schema(doc, count=count, seed=seed, locale=locale)
        else:
            click.secho(f"[Error] Schema type '{stype}' is not supported in this version.", fg="red")
            click.secho("Supported types: people, ecommerce", fg="yellow")
            sys.exit(1)
    else:
        if preset == "people":
            if mode == "streaming":
                if verbose:
                    click.echo("[Verbose] Using streaming mode for people preset.")
                click.secho("Generating in streaming mode...", fg="yellow")
                from .modes.streaming import generate_stream, people_stream
                generate_stream(people_stream, out, count=count, chunksize=chunksize, fmt=fmt, seed=seed, locale=locale)
                click.secho(f"Generated {count} records in {out}", fg="green")
                return
            else:
                if verbose:
                    click.echo("[Verbose] Using in-memory mode for people preset.")
                df = people_gen.generate_default(count=count, seed=seed, locale=locale)
        elif preset == "ecommerce":
            customers_df = None
            if customers_file:
                import pandas as pd
                try:
                    if customers_file.lower().endswith(".csv"):
                        customers_df = pd.read_csv(customers_file)
                    elif customers_file.lower().endswith(".json"):
                        customers_df = pd.read_json(customers_file)
                    else:
                        click.secho("[Error] Unsupported customers file format. Use CSV or JSON.", fg="red")
                        click.secho("Tip: Provide a .csv or .json file for --customers-file.", fg="yellow")
                        sys.exit(1)
                    if verbose:
                        click.echo(f"[Verbose] Loaded customers file: {customers_file}")
                except Exception as e:
                    click.secho(f"[Error] Failed to load customers file: {e}", fg="red")
                    click.secho("Tip: Ensure the file exists and is a valid CSV or JSON.", fg="yellow")
                    sys.exit(1)
                # Check required columns
                required_cols = {"customer_id", "name", "email"}
                if not required_cols.issubset(set(customers_df.columns)):
                    click.secho(f"[Error] Customers file must contain columns: {', '.join(required_cols)}.", fg="red")
                    click.secho("Tip: Check your CSV/JSON header.", fg="yellow")
                    sys.exit(1)
            if verbose:
                click.echo("[Verbose] Generating ecommerce data.")
            df = ecommerce_gen.generate_default(count=count, customers_df=customers_df, seed=seed, locale=locale)
        else:
            click.secho(f"[Error] Preset '{preset}' is not supported in this version.", fg="red")
            click.secho(f"Supported presets: {', '.join(PRESETS)}", fg="yellow")
            sys.exit(1)

    if mode == "testers":
        if verbose:
            click.echo("[Verbose] Injecting errors into dataset.")
        from .modes.testers import inject_errors
        df = inject_errors(df, error_rate=error_rate)

    # support streaming from a large df (writes in chunks)
    if mode == "streaming" and df is not None:
        if verbose:
            click.echo("[Verbose] Saving DataFrame in streaming mode.")
        save_df_stream(df, out, fmt=fmt, chunksize=chunksize)
    else:
        if verbose:
            click.echo("[Verbose] Saving DataFrame in memory mode.")
        save_df(df, out, fmt)

    click.secho(f"Generated {len(df)} records in {out}", fg="green")