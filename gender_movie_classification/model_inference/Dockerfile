FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ./
COPY ./model/pipeAPIclf.pkl /opt/ml/model/

COPY modules/ ./modules/
COPY app.py ./

RUN pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt -t .

RUN mkdir -p /var/task/nltk_data
COPY nltk_data/ /var/task/nltk_data 

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]