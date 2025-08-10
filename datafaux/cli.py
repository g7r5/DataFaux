import click
import sys
import yaml
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
def generate(preset, schema, count, out, fmt, seed, locale, mode, error_rate, chunksize):
    """Generate dataset with preset or schema"""
    if not preset and not schema:
        click.secho("Error: specify --preset or --schema", fg="red")
        sys.exit(1)

    df = None

    if schema:
        with open(schema, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        ok, msg = validate_schema(doc)
        if not ok:
            click.secho(f"Invalid schema: {msg}", fg="red")
            sys.exit(1)
        stype = doc.get("type")
        if stype == "people":
            # generate as DataFrame in memory (or streaming below)
            df = people_gen.generate_from_schema(doc, count=count, seed=seed, locale=locale)
        elif stype == "ecommerce":
            df = ecommerce_gen.generate_from_schema(doc, count=count, seed=seed, locale=locale)
        else:
            click.secho(f"Schema type {stype} not yet supported.", fg="red")
            sys.exit(1)
    else:
        if preset == "people":
            if mode == "streaming":
                # use streaming generator
                click.secho("Generating in streaming mode...", fg="yellow")
                from .modes.streaming import generate_stream, people_stream
                generate_stream(people_stream, out, count=count, chunksize=chunksize, fmt=fmt, seed=seed, locale=locale)
                click.secho(f"Generated {count} records in {out}", fg="green")
                return
            else:
                df = people_gen.generate_default(count=count, seed=seed, locale=locale)
        elif preset == "ecommerce":
            df = ecommerce_gen.generate_default(count=count, seed=seed, locale=locale)
        else:
            click.secho(f"Preset {preset} not yet supported in this version.", fg="red")
            sys.exit(1)

    if mode == "testers":
        from .modes.testers import inject_errors
        df = inject_errors(df, error_rate=error_rate)

    # support streaming from a large df (writes in chunks)
    if mode == "streaming" and df is not None:
        save_df_stream(df, out, fmt=fmt, chunksize=chunksize)
    else:
        save_df(df, out, fmt)

    click.secho(f"Generated {len(df)} records in {out}", fg="green")