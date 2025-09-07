[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/es/)
[![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)](https://peps.python.org/pep-0596/#schedule-first-bugfix-release)
[![Scikit Learn](https://img.shields.io/badge/scikit%20learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://github.com/scikit-learn/scikit-learn)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/amazon/aws-lambda-python)
[![Json](https://img.shields.io/badge/json-5E5C5C?style=flat-square&logo=json&logoColor=white)](gender_movie_classification/events/event.json)
[![Hoppscotch](https://img.shields.io/badge/Hoppscotch-31C48D?style=flat-square&logo=hoppscotch&logoColor=white)](https://hoppscotch.io/)
![GitHub last commit](https://img.shields.io/github/last-commit/HubertRonald/GenderMovieClassification?style=flat-square)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/HubertRonald/GenderMovieClassification?style=flat-square&color=dodgerblue)


# GenderMovieClassification  

Embedding y vectorización de texto para la clasificación de géneros de películas, desplegado en **AWS** con una arquitectura **serverless**.

El proyecto combina técnicas de **NLP** (tokenización, TF-IDF, embeddings) y algoritmos de **machine learning** con un enfoque de **MLOps**, empaquetado en contenedores **Docker** y orquestado mediante **AWS Lambda** y **API Gateway**.  


# GenderMovieClassification

## Infraestructura - IaC
El respositorio actual permite desplegar la siguiente arquitectura para disponibilizar un modelo que clasifica genero de peliculas, previamente calibrado utilizando solo la bilbioteca de sklearn.

![](./src/aws_apiRest_serverless_model.png)

## Pipeline: Preprocesamiento y Modelo Predictivo

El pipeline que se [serializó](./gender_movie_classification/model_inference/model/) fue el que se muestra a continuación

<div style="text-align:center"><img width="60%" src="./src/Pipeline.png" /></div>

El modelo serializado (pipeline) comprende lo pasos ya mencionados anteriormente:

### A. Preprocesamiento
#### **Tokenización**

1. La tokenización de palabras es un proceso fundamental en el pre procesamiento de texto para modelos de aprendizaje automático (ML) y procesamiento del lenguaje natural (PLN), es un paso crucial que transforma el texto en una forma adecuada para el análisis y el modelado mediante técnicas de aprendizaje automático.
   
#### **Unión de Características** 

Útil para combinar varios mecanismos de extracción de características en un solo transformador.

1. **El CountVectorizer:** Convierte texto en una matriz de conteos de palabras. Es útil para obtener la frecuencia de términos sin considerar su importancia relativa.
2. **El TFIDVectorizer:** Convierte texto en una matriz ponderada por TF-IDF, capturando tanto la frecuencia de términos como su importancia relativa. Es útil para manejar problemas de alta frecuencia de términos comunes y baja frecuencia de términos raros.
3. **El DictVectorizer:** Convierte diccionarios de características en matrices de características, útil para datos estructurados y categóricos que ya están en formato de diccionario.convierte una lista de diccionarios (donde cada diccionario representa una muestra y sus características) en una matriz de características.

#### **ToDense**
Convertir las matrices en arreglos.

#### **Normalizar**
Escala los vectores de entrada individualmente a la norma unitaria (longitud del vector).

### B. Modelo
#### **Stacking Classifer**

1. **Modelos Predictivos**
   - **Modelo MultinomialNB:** El modelo asume que los datos de entrada son distribuidos según una distribución multinomial, lo cual es adecuado para datos de conteos de palabras o frecuencias de palabras. Calcula las probabilidades de las características (palabras) dadas las clases y utiliza estas probabilidades para predecir la clase más probable para un nuevo documento. En lugar de usar las probabilidades de las características dadas las clases, ComplementNB utiliza las probabilidades complementarias, es decir, la probabilidad de una característica dada todas las clases excepto la clase actual.
   - **Modelo ComplementNB:** El modelo ComplementNB está diseñado para corregir algunas de las debilidades de MultinomialNB, especialmente cuando se trata de clases desbalanceadas.

    Combinar ambos modelos puede capturar diferentes aspectos de los datos y mejorar la precisión global mejorando el rendimiento del modelo, puede reducir la varianza y aumentar la estabilidad de las predicciones, y ComplementNB puede compensar los sesgos introducidos por MultinomialNB, especialmente en clases desbalanceadas.

2. **Resultado Final**
   - **Modelo Regresión Logística:** Incorporar una regresión logística multiclase como estimador final en un pipeline después de usar ambos modelos (MultinomialNB y ComplementNB) puede ser una estrategia efectiva para mejorar el rendimiento de clasificación. La regresión logística multiclase toma las predicciones de probabilidad (o las clases predichas) de MultinomialNB y ComplementNB como entradas. Se entrena para aprender cómo estas predicciones deben combinarse para mejorar la precisión global. En la fase de predicción, cada modelo base genera una predicción para un nuevo dato. El meta-modelo utiliza estas predicciones para generar la predicción final, aprovechando la información de ambos modelos base.

## Desplegando el Servicio

Se efectuan los siguientes pasos:

```mermaid
%%{init: {"flowchart": {"htmlLabels": false}} }%%
flowchart LR
    1["`**Paso 1**
    Cuenta de AWS
    Cloud9
    `"]
    2["`**Paso 2**
    Arquetipo
    _sam init_`"]
    3["`**Paso 3**
    Credenciales ECR
    `"]
    4["`**Paso 4**
    Imagen en ECR
    `"]
    5["`**Paso 5**
    Desplegar
    _sam build --guided_
    `"]
    6["`**Paso 6**
    Wizard
    `"]
    7["`**Paso 7**
    Confirmar
    `"]
    1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7
```

1. Al ingresar a AWS se levanta el servicio cloud9, con una instancia EC2 de por lo menos t3.medium y se clona este respositorio
   ```bash
   git clone https://github.com/HubertRonald/GenderMovieClassification.git
   ```
2. Ingresar al directorio donde está el arquetipo y compilar el servicio con `sam`, más información [aquí](./gender_movie_classification/README.md)
   ```bash 
   cd GenderMovieClassification/gender_movie_classification
   sam init
   ```
> **Nota:** Este paso 2 es opcional si ya se tiene el arquetipo efectuar el sam build, si en caso se tuvieran varias imagenes de docker en model_inference usar `prune` (`docker container prune -f`, `docker image prune -a -f`, `docker volume prune -f`, `docker network prune -f`) y validar espacio en disco `df -h`.

3. Como se requiere levantar el servicio ECR, para ello es necesario saber cuál es nuestro **accountID** (`$ aws configure list`) y la **region** que se emplea habitualmente para la cuenta antes encontrada (`$ aws sts get-caller-identity --query Account --output text`)
    ```bash
    aws --region <region> ecr get-login-password | docker login \
        --username AWS \
        --password-stdin <accountID>.dkr.ecr.<region>.amazonaws.com
    ```
4. Crear el respositorio de la imagen con el nombre de `gender-movie-classification`
    ```bash
    aws ecr create-repository \
      --repository-name "gender-movie-classification" \
      --image-tag-mutability MUTABLE \
      --image-scanning-configuration scanOnPush=true
    ```

    > Se obtiene el **"repositoryUri"**:
`<region>.dkr.ecr.us-east-1.amazonaws.com/gender-movie-classification`

1. Se despliega con `sam`, más información [aquí](./gender_movie_classification/README.md)
  ```bash
  sam deploy --guided
  ```
1. Diligenciar el wizard
    ```bash
    Configuring SAM deploy
    ======================

          Looking for config file [samconfig.toml] :  Found
          Reading default arguments  :  Success

          Setting default arguments for 'sam deploy'
          =========================================
          Stack Name [GenderMovieClassification]: GenderMovieClassification
          AWS Region [us-east-1]: us-east-1
          #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
          Confirm changes before deploy [Y/n]: Y
          #SAM needs permission to be able to create roles to connect to the resources in your template
          Allow SAM CLI IAM role creation [Y/n]: Y
          #Preserves the state of previously provisioned resources when an operation fails
          Disable rollback [y/N]: N
          ModelInferenceFunction has no authentication. Is this okay? [y/N]: y
          Save arguments to configuration file [Y/n]: n

          Looking for resources needed for deployment:
          Creating the required resources...
    ```

2. Confirmar despliegue de plantilla compilada en clouformation.


## Consumiendo API

Para obtener (método **GET**) la clasificación(es) del genero de una película a partir del modelo previamente industrializado, se tienen las siguientes opciones:

1. En la barra del navegador de tu preferencia

    |Ejemplos | URL |
    |---|---|
    |Ejemplo 1 - E1|https://71qrz15jz2.execute-api.us-east-1.amazonaws.com/Prod/inference?plot=who%20meets%20by%20fate%20,%20%20shall%20be%20sealed%20by%20fate%20.%20%20theresa%20osborne%20is%20running%20along%20the%20beach%20when%20she%20stumbles%20upon%20a%20bottle%20washed%20up%20on%20the%20shore%20.%20%20inside%20is%20a%20message%20,%20%20reading%20the%20letter%20she%20feels%20so%20moved%20and%20yet%20she%20felt%20as%20if%20she%20has%20violated%20someone%20%27%20s%20thoughts%20.%20%20in%20love%20with%20a%20man%20she%20has%20never%20met%20,%20%20theresa%20tracks%20down%20the%20author%20of%20the%20letter%20to%20a%20small%20town%20in%20wilmington%20,%20%20two%20lovers%20with%20crossed%20paths%20.%20%20but%20yet%20one%20can%20%27%20t%20let%20go%20of%20their%20past%20 |
    |Ejemplo 2 - E2|https://71qrz15jz2.execute-api.us-east-1.amazonaws.com/Prod/inference?plot=the%20true%20story%20of%20billy%20hayes%20,%20%20an%20american%20college%20student%20who%20is%20caught%20smuggling%20drugs%20out%20of%20turkey%20and%20thrown%20into%20prison%20| 

    Endpoint método **GET**
    ```bash
    https://71qrz15jz2.execute-api.us-east-1.amazonaws.com/Prod/inference
    ```
    Seguido del simbolo **?** y de cada **parametro=valor** unido por **&** (solo es el plot)
    
    ```bash
    plot=<valor>
    ```
    >**Nota:** reemplazar \<valor> según el parámetro el plot de la película pero reemplazando los espacios en blanco con `%20` aquí un codigo en python

    ```python
    import pandas as pd

    dataTesting = pd.read_csv('https://github.com/albahnsen/MIAD_ML_and_NLP/raw/main/datasets/dataTesting.zip', encoding='UTF-8', index_col=0)

    index = 4 # el de tu preferencia
    data = dataTesting.loc[dataTesting['plot'].index==index, 'plot']

    # Obtener Endpoint
    print(url+'?plot='+data.values[0].replace(' ','%20'))
    ```

2. Empleando [hoppscotch](https://hoppscotch.io/) (servicio similar a **postman** pero online)

    En ambos ejemplos puede ser necesario aplicar un paso 7, para habilitar el proxy

    **Paso 7 (Proxy)**

    *Interceptador: Proxy*
    ![](./src/7org.png)

    **Ejemplo 1 - E1**

    *Formulario E1*
    ![](./src/11org.png)


    **Ejemplo 2 - E2**

    *Formulario E2*
    ![](./src/21org.png)
    

    Para la carga masiva mostradas en las imagenes de arriba
    |Ejemplo 1 - E1 | Ejemplo 2 - E2 |
    |---|---|
    |plot:who meets by fate ,  shall be sealed by fate .  theresa osborne is running along the beach when she stumbles upon a bottle washed up on the shore .  inside is a message ,  reading the letter she feels so moved and yet she felt as if she has violated someone ' s thoughts .  in love with a man she has never met ,  theresa tracks down the author of the letter to a small town in wilmington ,  two lovers with crossed paths .  but yet one can ' t let go of their past .|plot:the true story of billy hayes ,  an american college student who is caught smuggling drugs out of turkey and thrown into prison .|

    Endpoint método **GET**
    ```bash
    https://71qrz15jz2.execute-api.us-east-1.amazonaws.com/Prod/inference
    ```

> **Nota:** Para los ejemplos 1 y 2, se obtienen las respuestas:

 |Ejemplo 1 - E1 | Ejemplo 2 - E2 |
|----|----|
| {'p_Action': 0.1269843577709364, 'p_Adventure': 0.04503903848273675, 'p_Animation': 0.020947927405038598, 'p_Biography': 0.02646010558429211, 'p_Comedy': 0.1839028668790464, 'p_Crime': 0.07302944407577226, 'p_Documentary': 0.01726944330701433, 'p_Drama': 0.48203848532551025, 'p_Family': 0.02939926867829299, 'p_Fantasy': 0.07397509969021411, 'p_Film-Noir': 0.022728826878362324, 'p_History': 0.02115209683073603, 'p_Horror': 0.08256868349777494, 'p_Music': 0.020615567211366495, 'p_Musical': 0.032903098767361014, 'p_Mystery': 0.12022016586870923, 'p_News': 0.0008491681958503885, 'p_Romance': 0.6348880133666133, 'p_Sci-Fi': 0.03594986283810206, 'p_Short': 0.011201190059057203, 'p_Sport': 0.01961336805897658, 'p_Thriller': 0.14076101845073516, 'p_War': 0.019790392501055205, 'p_Western': 0.022510890723811967} | {'p_Action': 0.13793797791608903, 'p_Adventure': 0.024351050038927714, 'p_Animation': 0.02184167137035558, 'p_Biography': 0.11084417912085025, 'p_Comedy': 0.3410877630863187, 'p_Crime': 0.25730853466447984, 'p_Documentary': 0.03547527270932129, 'p_Drama': 0.8218692320838602, 'p_Family': 0.016374451280989178, 'p_Fantasy': 0.015129663543233744, 'p_Film-Noir': 0.01637423764028967, 'p_History': 0.03290802792973829, 'p_Horror': 0.06074156261628383, 'p_Music': 0.026682122082855232, 'p_Musical': 0.030532221812221188, 'p_Mystery': 0.03256048830412039, 'p_News': 0.0010730730945814383, 'p_Romance': 0.054874605166701035, 'p_Sci-Fi': 0.016813367898715983, 'p_Short': 0.011211576793558905, 'p_Sport': 0.02712776433049964, 'p_Thriller': 0.3136007103316439, 'p_War': 0.04848235407652713, 'p_Western': 0.02048935493512432} |


## Eliminar Recursos

1. Eliminar imagen de docker en el ECR
  ```bash
  aws ecr delete-repository --registry-id <account-id> --repository-name gender-movie-classification --force
  ```

2. Eliminar stack desde `sam`, más informacio [aquí](./gender_movie_classification/README.md)
```bash
sam delete --stack-name "GenderMovieClassification"
```

3. Finalmente en `S3` eliminar aquel bucket creado por `sam` cuyo nombre contenga `GenderMovieClassification`, hacer lo propio en `cloudformation`

## Fuentes

Documentación consultada y complementaria

1. [Deploying machine learning models with serverless templates](https://aws.amazon.com/es/blogs/compute/deploying-machine-learning-models-with-serverless-templates/)
2. [Serverless Rest API on AWS with Lambda and API Gateway using SAM (Serverless Application Model)](https://apoorv487.medium.com/serverless-rest-api-on-aws-with-lambda-and-api-gateway-using-sam-serverless-application-model-4aa3b550be1d)
3. [AWS Lambda Now Supports Up to 10 GB Ephemeral Storage](https://aws.amazon.com/es/blogs/aws/aws-lambda-now-supports-up-to-10-gb-ephemeral-storage/)

Para modelos predictivos más pequeños (sin docker)

4. [Deploying a Machine Learning Model to a Serverless Backend with SAM CLI](https://medium.com/carnegie-mellon-robotics-academy/going-serverless-for-your-ml-backend-with-sam-cli-5332912019ef)
