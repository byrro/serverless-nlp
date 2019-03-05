'''Constant values needed by the application'''
import os


# Data types accepted by the spaCy Lambda function
VALID_DATA_TYPES = [
    'sentence',
    'part-of-speech',
    'named-entity',
]

# Set default values for spaCy Lambda name and AWS region
DEFAULT_SPACY_LAMBDA_NAME = 'serverless-nlp-spacy'
DEFAULT_SPACY_LAMBDA_REGION = 'us-east-1'

# Check whether custom values for spaCy Lambda name and region were set
ENV_SPACY_LAMBDA_NAME = os.environ.get('SPACY_LAMBDA_NAME')
ENV_SPACY_LAMBDA_REGION = os.environ.get('SPACY_LAMBDA_REGION')

# Auto set default values
if type(ENV_SPACY_LAMBDA_NAME) is not str:
    ENV_SPACY_LAMBDA_NAME = DEFAULT_SPACY_LAMBDA_NAME

if type(ENV_SPACY_LAMBDA_REGION) is not str:
    ENV_SPACY_LAMBDA_REGION = DEFAULT_SPACY_LAMBDA_REGION
