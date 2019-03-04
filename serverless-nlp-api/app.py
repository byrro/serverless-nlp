'''API to serve requests for Natural Language Processing Lambda function'''
import json
from chalice import Chalice
from chalicelib.api_handler import APIHandler
from chalicelib.app_logger import log


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
    :arg model: (str) name of spaCy model to use
    '''
    try:
        args = app.current_request.json_body

        handler = APIHandler(
            data_type=args.get('data_type'),
            text=args.get('text'),
            model=args.get('model'),
        )

        response = handler.process()

        return {
            'status': response['status'],
            'message': response['message'],
            'request': {
                'args': args,
            },
            'acknowledgement': 'Dashbird.io - Observability tool for '
                               'serverless applications.',
            'data': response['data'],
        }

    except Exception as error:
        # Log the error encountered
        log(error=error)

        # Log the user request for debugging purposes
        # JSON format makes it easier to visualize on CloudWatch or Dashbird
        print('app.current_request:')
        print(json.dumps(app.current_request.to_dict()))

        return {
            'status': 500,
            'message': 'Oops, there was an internal error! :(',
        }
