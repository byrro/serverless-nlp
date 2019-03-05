'''API to serve requests for Natural Language Processing Lambda function'''
import json
from chalice import Chalice
from chalicelib.api_handler import request_handler


app = Chalice(app_name='serverless-nlp-api')


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Entry endpoint with basic description of the application
    '''
    return {
        'application': 'serverless-nlp',
        'description': 'Serverless implementation of a Natural Language '
                       'Processing (NLP) service powered by the spaCy open '
                       'source framework.',
        'source': 'https://github.com/byrro/serverless-nlp',
        'documentation': '',
        'acknowledgement': {
            'name': 'Dashbird',
            'url': 'https://dashbird.io/',
            'description': 'This implementation of spaCy for AWS Lambda is '
                           'offered by Dashbird, a monitoring and debugging '
                           'service designed for serverless applications.',
        },
        'credits': {
            'api-service': {
                'name': 'AWS Chalice',
                'url': 'https://github.com/aws/chalice',
                'decription': 'Chalice is a microframework for writing '
                              'serverless apps in python. It allows you to '
                              'quickly create and deploy applications that '
                              'use AWS Lambda.',
            },
            'natural-language-processing': {
                'name': 'Explosion spaCy',
                'url': 'https://github.com/explosion/spaCy',
                'description': 'spaCy is a library for advanced Natural '
                               'Language Processing in Python and Cython. '
                               'It\'s built on the very latest research, and '
                               'was designed from day one to be used in real '
                               'products.',
            },
        },
    }


@app.route('/extract', methods=['POST'])
def extract():
    '''Main endpoint to request extraction of data from a text

    Expects a JSON in the body with the following arguments:
    :arg text: (str) text body to process
    :arg data_type: (str) type of data to extract - options are:
        'sentence'
        'part-of-speech'
        'named-entity'
    :arg model_name: (str) name of spaCy model to use
    '''
    return request_handler(app=app)


@app.route('/example/{data_type}', methods=['GET', 'POST'])
def example(data_type):
    req_args = {
        'data_type': data_type,
        'text': 'Lambda is an event-driven, serverless computing platform provided by Amazon as a part of the Amazon Web Services. It is a computing service that runs code in response to events and automatically manages the computing resources required by that code. It was introduced in November 2014. Headquartered in Seattle, USA and leaded by Andy Jassy (CEO), Amazon Web Services made $17.4 billion in revenue and $4.331 billion in profits in the year of 2017. Source: Wikipedia.org.',  # NOQA
        'model_name': 'en_core_web_sm',
    }

    return request_handler(app=app, req_args=req_args)
