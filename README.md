# Debian Contents Parser

## Overview

Very basic Python package to parse Debian Contents files.

Easiest way to run the code is to create a virtual environment, install the package to the environment with pip and then run through the exposed entry-point cli commands. See [Setup-tools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html) for more information on the package management system.

Install via:

```bash
python -m venv .venv
# Activate your environemt with:
#      `source .venv/bin/activate` on Unix/macOS
# or   `.venv\Scripts\activate` on Windows
pip install --editable .
```

Run with the following commands, making sure to source the environment created above FIRST:

```bash
contents-parser -a amd64
# Run contents-parser --help for more info
```
