import json
import pytest
from model_inference import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": {
            "data": {
                    "plot": "the true story of billy hayes ,  an american college student who is caught smuggling drugs out of turkey and thrown into prison .",
                }
            }
    }


def test_lambda_handler(apigw_event):

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret['body'])

    assert ret["statusCode"] == 200
