# Pagey

**TL;DR:** Pagey is a Pagerduty slack bot.


[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/slackbot-pagey)](https://pypi.org/project/slackbot-pagey/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slackbot-pagey)](https://pypi.org/project/slackbot-pagey/)
[![PyPI - Format](https://img.shields.io/pypi/format/slackbot-pagey)](https://pypi.org/project/slackbot-pagey/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/slackbot-pagey)](https://pypi.org/project/slackbot-pagey/)
[![PyPI - License](https://img.shields.io/pypi/l/slackbot-pagey)](https://pypi.org/project/slackbot-pagey/)


## :hourglass: Pipelines

[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/linting/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=linting)
[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/building/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=building)
[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/testing/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=testing)

[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/black/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=black)
[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/bandit/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=bandit)
[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/mypy/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=mypy)
[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/pylint/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=pylint)
[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/pycode/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=pycode)
[![Build Status](https://github.com/Flaconi/slackbot-pagey/workflows/pydoc/badge.svg)](https://github.com/Flaconi/slackbot-pagey/actions?workflow=pydoc)



## :tada: Install
```bash
pip install pagey
```

> :exclamation: Requires Python >= 3.6


## :computer: Usage
```bash
# Export required tokens to your env
export PAGEY_SLACK_TOKEN="read-write slack token"
export PAGEY_PD_TOKEN="read-only pagerduty token"

# Run it
pagey
```


## :page_facing_up: License

**[MIT License](LICENSE.txt)**

Copyright (c) 2021 **[Flaconi](https://github.com/Flaconi)**
