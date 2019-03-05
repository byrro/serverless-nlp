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
        environ='local' if not context else 'aws',
    )

    return response


if __name__ == '__main__':
    lambda_handler(
        event={
            'data_type': 'named-entity',
            'text': 'Lambda is an event-driven, serverless computing platform provided by Amazon as a part of the Amazon Web Services. It is a computing service that runs code in response to events and automatically manages the computing resources required by that code. It was introduced in November 2014. Headquartered in Seattle, USA and leaded by Andy Jassy (CEO), Amazon Web Services made $17.4 billion in revenue and $4.331 billion in profits in the year of 2017. Source: Wikipedia.org.',  # NOQA
            'model_name': 'en_core_web_sm',
        },
        context=None,
    )
