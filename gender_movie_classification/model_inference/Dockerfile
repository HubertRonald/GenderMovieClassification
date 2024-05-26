FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ./
COPY ./model/pipeAPIclf.pkl /opt/ml/model/

RUN pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt -t .
RUN python3.9 -c "import nltk; nltk.download('stopwords')"

COPY ./modules ./
COPY app.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]