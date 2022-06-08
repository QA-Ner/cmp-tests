# CMP Tests Automation with Python+Playwright+Pytest

- features of MS Playwright on Python
- automation project structure using pytest


Tools:

- [Playwright](https://github.com/microsoft/playwright-python)
- [Pytest](https://pytest.org/)

## Install guide

1. Install python
2. Install PyCharm
3. Install python dependencies
   `pip install -r requirements.txt`
4. Make sure playwright version 1.8+ installed

## Project structure

- [conftest.py](conftest.py) file contains main fixtures to work
- Page objects stored in page_object folder
- Tests stored in tests folder
- Settings are spread between:
    - pytest.ini
    - settings.py

## Run guide
Run tests using command `pytest`


