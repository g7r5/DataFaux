from setuptools import setup, find_packages

setup(
    name='datafaux',
    version='0.1.0',
    description='Generador de datos ficticios para pruebas y desarrollo',
    author='Jean-EstevezT',
    packages=find_packages(),
    install_requires=[
        'faker',
        'pandas',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'datafaux=datafaux.main:main',
        ],
    },
)
