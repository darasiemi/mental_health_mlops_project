FROM public.ecr.aws/lambda/python:3.11

RUN pip install -U pip
RUN pip install pipenv

RUN mkdir -p /app/integration-tests

COPY ["tests/integration-tests/Pipfile", "tests/integration-tests/Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY model/ /app/integration-tests/model/
COPY utils/ /app/integration-tests/utils/
COPY vectorizer/ /app/integration-tests/vectorizer/

# RUN echo "The working directory:" && pwd

COPY ["tests/integration-tests/lambda_function.py", "/app/integration-tests/utils"]

ENV PYTHONPATH="/app:/app/integration-tests:/app/integration-tests/utils:$PYTHONPATH"

# RUN echo "Directory structure of /app:" && ls -R /app

WORKDIR /app/integration-tests/utils

CMD ["lambda_function.lambda_handler"]
