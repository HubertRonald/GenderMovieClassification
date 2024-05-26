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

RUN python3.9 -m pip install -r requirements.txt -t . --no-cache-dir --progress-bar=on || (echo "Entering shell for debugging" && /bin/sh)
RUN python3.9 -c "import nltk; import os; nltk.download('stopwords', download_dir=os.getenv('NLTK_DATA'))"

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]