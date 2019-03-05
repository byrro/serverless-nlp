'''Handler of API requests'''
import json
from chalicelib.app_logger import log
from chalicelib import constants as c
from chalicelib.lambda_function import lambda_spacy


class APIHandler():
    '''Handles API requests
    '''
    def __init__(self, data_type, text, model_name):
        self.data_type = data_type
        self.text = text
        self.model_name = model_name

        if type(self.data_type) is not str or \
                self.data_type not in c.VALID_DATA_TYPES:
            valid = '", "'.join(c.VALID_DATA_TYPES)
            raise ValueError('"data_type" is invalid - expected one of these '
                             f'options: "{valid}".')

        if type(self.text) is not str:
            raise ValueError('"text" is invalid - extected "str", got '
                             f'"{type(self.text)}".')

        if type(self.model_name) is not str:
            raise ValueError('"model" is invalid - extected "str", got '
                             f'"{type(self.model_name)}".')

    def process(self):
        '''Process an API request
        '''
        return lambda_spacy.invoke(
            event={
                'data_type': self.data_type,
                'text': self.text,
                'model_name': self.model_name,
            },
        )


def request_handler(app, req_args=None):
    try:
        if not req_args:
            req_args = app.current_request.json_body

        handler = APIHandler(
            data_type=req_args.get('data_type'),
            text=req_args.get('text'),
            model_name=req_args.get('model_name'),
        )

        response = handler.process()

        return {
            'status': response['status'],
            'message': response['message'],
            'request': {
                'args': req_args,
            },
            'acknowledgement': 'This open-source implementation is offered by '
                               'Dashbird.io, the coolest monitoring and '
                               'debugging tool for serverless applications.',
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
