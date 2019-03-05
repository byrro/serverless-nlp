'''Implement logic to handle Lambda invocation requests'''
import json
import botocore
from nlp import SpacyWrapper
from app_logger import log


def request_handler(event, context, environ):
    '''Handles Lambda invocation requests
    '''
    try:
        # Log the request payload event for debugging and monitoring purposes
        print('REQUEST PAYLOAD EVENT:')
        print(json.dumps(event))
        print('')

        # Instantiate spaCy wrapper
        spacy_nlp = SpacyWrapper(environ=environ)

        # Extract NLP data requested
        data = spacy_nlp.extract(
            data_type=event.get('data_type'),
            text=event.get('text'),
            model_name=event.get('model_name'),
        )

        # Prepare success response info
        status = 200
        message = 'NLP data successfully extracted'

    # Botocore exception
    except botocore.exceptions.ClientError as error:
        log(error=error)

        if 'Not Found' in str(error):
            status = 400
            message = 'spaCy model not found'
            data = None

        else:
            status = 500
            message = 'Oops, there was an internal error!'
            data = None

    # Generic exception raised
    except Exception as error:
        log(error=error)

        status = 500
        message = 'Oops, there was an internal error!'
        data = None

    finally:
        response = {
            'status': status,
            'message': message,
            'data': data,
        }

        print('')
        print('RESPONSE:')
        print(json.dumps(response))

        return response
