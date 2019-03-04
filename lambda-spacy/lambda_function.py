'''Entry point script for the AWS Lambda function'''
from app_handler import request_handler


def lambda_handler(event, context):
    '''Invocation handler for the Lambda function

    :arg event: (dict) event payload provided by the invoker
    :arg context: (dict) runtime context provided by AWS Lambda environment
    '''
    response = request_handler(
        event=event,
        context=context,
    )

    return response


if __name__ == '__main__':
    request_handler(
        event={
            'data_type': 'named-entity',
            'text': 'With AWS Lambda, we get scalability and resilience out-of-the-box. What’s more, AWS also provides built-in monitoring, logging and tracing support through CloudWatch and X-Ray. These built-in tools provide a good starting point but many developers eventually outgrow them as their serverless application becomes more complex.',
            'model_name': 'en_core_web_sm',
        },
        context=None,
    )
