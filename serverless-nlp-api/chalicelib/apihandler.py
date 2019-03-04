'''Handler of API requests'''
from chalicelib import constants as c
from chalicelib.awslambda import lambda_spacy


class APIHandler():
    '''Handles API requests
    '''
    def __init__(self, data_type, text, model):
        self.data_type = data_type
        self.text = text
        self.model = model

        if type(self.data_type) is not str or \
                self.data_type not in c.VALID_DATA_TYPES:
            valid = '", "'.join(c.VALID_DATA_TYPES)
            raise ValueError('"data_type" is invalid - expected one of these '
                             f'options: "{valid}".')

        if type(self.text) is not str:
            raise ValueError('"text" is invalid - extected "str", got '
                             f'"{type(self.text)}".')

        if type(self.model) is not str:
            raise ValueError('"model" is invalid - extected "str", got '
                             f'"{type(self.model)}".')

    def process(self):
        '''Process an API request
        '''
        return lambda_spacy.invoke(
            event={
                'data_type': self.data_type,
                'text': self.text,
                'model': self.model,
            },
        )
