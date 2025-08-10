from setuptools import setup, find_packages

setup(
    name="datafaux",
    version="0.1.0",
    description="DataFaux - Test dataset generator (restructured)",
    packages=find_packages(),
    install_requires=[
        "faker>=19.0.0",
        "pandas>=2.0.0",
        "pyyaml",
        "click",
        "openpyxl",
        "pyarrow",
        "fastparquet",
    ],
    entry_points={
        "console_scripts": [
            "datafaux=datafaux.cli:main"
        ]
    },
)