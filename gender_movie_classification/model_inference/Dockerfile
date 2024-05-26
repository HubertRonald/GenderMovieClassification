FROM public.ecr.aws/lambda/python:3.9

# Definir la variable de entorno temporal para NLTK_DATA
ENV MODEL_PATH="/opt/ml/model/"
ENV NLTK_DATA="/var/task/nltk_data"

COPY requirements.txt ./
COPY ./model/pipeAPIclf.pkl /opt/ml/model/
COPY modules/ ./modules/
COPY app.py ./

RUN mkdir -p /var/task/nltk_data
RUN pip install --upgrade pip

RUN python3.9 -m pip install -r requirements.txt -t .
COPY nltk_data/ /var/task/nltk_data 

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]