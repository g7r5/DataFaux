
def test_invalid_schema(tmp_path):
	# Write an invalid schema (missing 'type')
	invalid_schema = tmp_path / "invalid_schema.yaml"
	invalid_schema.write_text("fields:\n  - name: foo\n    type: bar\n")
	out_path = tmp_path / "out.csv"
	result = subprocess.run([
		"python", "-m", "datafaux.main", "generate",
		"--schema", str(invalid_schema),
		"--count", "5",
		"--out", str(out_path)
	], capture_output=True, text=True)
	assert result.returncode != 0
	assert "Invalid schema" in result.stderr or "Error" in result.stderr
# Test CLI for ecommerce preset with --customers-file
import os
import tempfile
import pandas as pd
import subprocess

def test_cli_ecommerce_with_customers():
	# Create a temporary customers CSV
	customers = pd.DataFrame([
		{"customer_id": "1", "name": "Alice", "email": "alice@example.com"},
		{"customer_id": "2", "name": "Bob", "email": "bob@example.com"}
	])
	with tempfile.TemporaryDirectory() as tmpdir:
		customers_path = os.path.join(tmpdir, "customers.csv")
		out_path = os.path.join(tmpdir, "orders.csv")
		customers.to_csv(customers_path, index=False)
		# Run the CLI command
		result = subprocess.run([
			"python", "-m", "datafaux.main", "generate",
			"--preset", "ecommerce",
			"--count", "5",
			"--out", out_path,
			"--customers-file", customers_path
		], capture_output=True, text=True)
		assert result.returncode == 0, f"CLI failed: {result.stderr}"
		assert os.path.exists(out_path)
		df = pd.read_csv(out_path)
		assert "customer_id" in df.columns
