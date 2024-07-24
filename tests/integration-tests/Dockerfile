FROM public.ecr.aws/lambda/python:3.11

RUN pip install -U pip
RUN pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY model/* ./model/

COPY utils/* ./utils/

COPY vectorizer/* ./vectorizer/

COPY [ "lambda_function.py", "./" ]

CMD [ "lambda_function.lambda_handler" ]
