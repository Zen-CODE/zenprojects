# Zen FastAPI POC

This project explores the FastAPI library.

## Running the App

The launch the app using uvicorn:

    uvicorn main:app --reload

## Tests

To run tests:

    cd app/
    coverage run --source=. -m pytest tests
    coverage report -m

## Tips

To open the Swagger docs: http://127.0.0.1:8000/swagger
