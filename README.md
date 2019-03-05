# serverless-nlp
Demo of a Serverless Natural Language Processing Service. This app uses:

- [spaCy](https://https://github.com/explosion/spaCy): deep learning NLP (natural language processing) library
- [Chalice](https://github.com/aws/chalice): serverless Python framework
- [AWS Lambda](https://aws.amazon.com/lambda/): FaaS compute service
- [API Gateway](https://aws.amazon.com/api-gateway/): API management service
- [Dashbird.io](https://dashbird.io/): monitoring, logging and anomaly detection

## Quick Demo

We've deployed a demo API for this application using [AWS Lambda](https://aws.amazon.com/lambda/) and [API Gateway](https://aws.amazon.com/api-gateway/).

You can try examples with a pre-determined text on these URLs:

- Sentence Extraction: [https://g5kl1e9fhf.execute-api.us-east-1.amazonaws.com/api/example/sentence](https://g5kl1e9fhf.execute-api.us-east-1.amazonaws.com/api/example/sentence)
- Named Entity Recognition: [https://g5kl1e9fhf.execute-api.us-east-1.amazonaws.com/api/example/named-entity](https://g5kl1e9fhf.execute-api.us-east-1.amazonaws.com/api/example/named-entity)
- Part-of-Speech Tagging: [https://g5kl1e9fhf.execute-api.us-east-1.amazonaws.com/api/example/part-of-speech](https://g5kl1e9fhf.execute-api.us-east-1.amazonaws.com/api/example/part-of-speech)

The text used for the examples above is:

> Lambda is an event-driven, serverless computing platform provided by Amazon as a part of the Amazon Web Services. It is a computing service that runs code in response to events and automatically manages the computing resources required by that code. It was introduced in November 2014. Andy Jassy is the CEO of Amazon Web Services. The company earned $17.4 billion in revenue and $4.331 billion in profits in the year of 2017. Source: Wikipedia.org.

To try the API with your own text sample, use cURL:

`curl -XPOST -H "Content-type: application/json" -d '{"data_type": "named-entity", "text": "Your text goes here!", "model_name": "en_core_web_sm"}' 'https://g5kl1e9fhf.execute-api.us-east-1.amazonaws.com/api/extract'`

In the `data_type` argument, you can provide:

- sentence
- named-entity
- part-of-speech

This demo API only supports text in English, having only one model deployed (en_core_web_sm). You can clone/fork this repo and deploy other [spaCy models](https://spacy.io/usage/models) to support multiple languages.

## Pre-requisites

- [Python 3.6+](https://www.python.org/downloads/release/python-370/)
- [pip 18.1+](https://pypi.org/project/pip/)
