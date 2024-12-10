```python
from setuptools import setup, find_packages

setup(
    name="nuclei-tools",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5==5.15.9',
        'PyYAML==6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'nuclei-tools=src.main:main',
        ],
    },
    python_requires='>=3.6',
)
```