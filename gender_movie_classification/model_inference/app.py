from modules.preprocesing import TokenText
from modules.preprocesing import TextToDictTransformer
from modules.preprocesing import ToDense
from modules.preprocesing import Normalize
from modules.fields import Fields

import json
import joblib
import pandas as pd


# import requests
def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """


    # read model (pipeline)
    path = '/opt/ml/model/'
    model_train = joblib.load(path+'pipeAPIclf.pkl')

    # read data
    try:
        # Obtener los datos del cuerpo de la solicitud
        if event['httpMethod'] == 'GET':
            # Obtener los parámetros de la cadena de consulta de la URL
            parameters = event['queryStringParameters']
            # Resto del código para procesar los parámetros
            plot = str(parameters.get('plot', ''))
            
        else:
            # Obtener los datos del cuerpo de la solicitud
            if 'body' in event:
                data = json.loads(event['body'])
            else:
                data = event

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    # predict
    data = pd.Series(data={'1': plot})
    cols = Fields().cols
    
    predictions = pd.DataFrame(
        data=model_train.predict_proba(data),
        columns=cols
    )

    res = dict(
        zip(cols, predictions.values[0])
    )
    
    # show predict
    return {
        "statusCode": 200,
        "body": dict(clasification=json.dumps(res)),
    }
