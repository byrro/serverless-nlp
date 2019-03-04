'''Code to interact with AWS Lambda functions'''
import copy
import json
import boto3
import botocore
from chalicelib.constants import (
    ENV_SPACY_LAMBDA_NAME,
    ENV_SPACY_LAMBDA_REGION,
)
from chalicelib.app_logger import log


class LambdaFn():
    '''Representation of an AWS Lambda allowing to interact with it

    :attr name: (str) name of the AWS Lambda function
    :attr region: (str) AWS region where the Lambda is deployed
    '''
    def __init__(self, name, region):
        '''Initializes the Lambda representation

        :arg name: (str) name of the AWS Lambda function
        :attr region: (str) AWS region where the Lambda is deployed
        '''
        self.function_name = name
        self.region = region
        self.response_template = {
            'status': None,
            'message': None,
            'data': None,
        }

    def invoke(
            self,
            event,
            log_type='None',
            invocation_type='RequestResponse'):
        '''Invokes the AWS Lambda function

        :arg invocation_type: (str) one of these options:
            'RequestResponse': synchronous call, will wait for Lambda to answer
            'Event': asynchronous call, will NOT wait for Lambda processing
            'DryRun': validate args values and user permission
        :arg payload: (dict) payload data to submit to the Lambda function
        :arg log_type: (str) one of these options:
            'None': does not include execution logs in the response
            'Tail': includes execution logs in the response
        '''
        session = boto3.session.Session()
        aws_lambda = session.client('lambda')

        # Invoke Lambda
        try:
            response = aws_lambda.invoke(
                FunctionName=self.function_name,
                InvocationType=invocation_type,
                LogType=log_type,
                Payload=json.dumps(event),
            )

            # Decode response payload
            try:
                payload = json.loads(
                    response['Payload'].read(amt=None).decode('utf-8')
                )

            except json.decoder.JSONDecodeError:
                payload = {}

        except aws_lambda.exceptions.ResourceNotFoundException as error:
            log(error=error)

            payload = {
                'status': 404,
                'message': f'Lambda "{self.function_name}" was not found in '
                           f'region "{self.region}".',
                'data': None,
            }

        # Populate response with Lambda payload
        response = copy.deepcopy(self.response_template)

        response['status'] = payload.get('status')
        response['message'] = payload.get('message')
        response['data'] = payload.get('data')

        return response


# Instantiate representation of spaCy Lambda function
lambda_spacy = LambdaFn(
    name=ENV_SPACY_LAMBDA_NAME,
    region=ENV_SPACY_LAMBDA_REGION,
)
