FROM public.ecr.aws/lambda/python:3.9

# Definir la variable de entorno temporal para NLTK_DATA
ENV MODEL_PATH="/opt/ml/model/"
ENV NLTK_DATA="/var/task/nltk_data"

COPY requirements.txt ./
COPY ./model/pipeAPIclf.pkl ${MODEL_PATH}
COPY modules/ ./modules/
COPY app.py ./

RUN mkdir -p ${NLTK_DATA}
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('stopwords', download_dir='/var/task/nltk_data')"

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]