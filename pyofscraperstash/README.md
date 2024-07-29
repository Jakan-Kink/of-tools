pyofscraperstash
================

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

Took massive inspiration from the [OFMetadataToStash](https://github.com/ALonelyJuicebox/OFMetadataToStash) PowerShell script that didn't work on ARM64.

Instead of using the command prompt to query the flow, everything will be in the config file (you can use either YAML or JSON).

To verify the config file before run, you can either include the `sanity_check: true` block, or include `--sanity-check` in the script parameters.

## How to use

First make sure that you have the needed dependancies:

```Python

poetry install --no-root
```

Make sure that your paths are updated in the `config.yml` file.

Then you should be able to run the program:

```bash

python3 pyofscraperstash/__main__.py -c config.yml
```

### Extra arguments

#### -a YYYY-MM-DD, --after YYYY-MM-DD

Will only look at data in the user_data.db files after the specified date.

#### -b YYYY-MM-DD, --before YYYY-MM-DD

Will only look at data in the user_data.db files before the specified date.

#### -md YYYY-MM-DD, --metadata-modification-date YYYY-MM-DD

Will only process user_data.db files modified after the specified date (and if you do not include a separate -a this date will also be used to not process older records in the db)

#### -c filename.ext, --config-file filename.ext

Tell it where the config file is located.

#### -i, --images-only

Process only image files listed in the db

#### -s, --scenes-only

Process only video files listed in the db

#### -v, --verbose

More verbose logging

#### -V, --version

Show the version number

#### --sanity-check

Also perform some checks to make sure that the config looks right before trying to process all of the databases.

<!-- For the date format in the OF-scraper portion of the config file, we are using the same [tokens from Arrow](https://arrow.readthedocs.io/en/latest/guide.html#supported-tokens) for compatibility. -->
