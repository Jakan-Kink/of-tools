pyOFscraperStash
================

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

Took massive inspiration from the [OFMetadataToStash](https://github.com/ALonelyJuicebox/OFMetadataToStash) PowerShell script that didn't work on ARM64.

Instead of using the command prompt to query the flow, everything will be in the config file (you can use either YAML or JSON).

To verify the config file before run, you can either include the `sanity_check: true` block, or include `--sanity-check` in the script parameters.

For the date format in the OF-scraper portion of the config file, we are using the same [tokens from Arrow](https://arrow.readthedocs.io/en/latest/guide.html#supported-tokens) for compatibility.
