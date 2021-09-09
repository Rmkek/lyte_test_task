Lyte test task
==============================

Running the project
------------
- `pipenv shell` (if you use it)
- `pip install -r requirements.txt` or `pipenv install` 
- `uvicorn main:app --reload`

Run tests
------------
- `pytest`
- `coverage run -m pytest`
- `coverage report`

Before commiting
------------
- `pre-commit install`
- `git commit` -- should run black automatically