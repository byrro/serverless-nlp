'''Wrapper for interacting with spaCy NLP models'''
import os
from zipfile import ZipFile
import boto3
import botocore
import spacy
import constants as c


class SpacyWrapper():
    '''Wrapper class for interacting with spaCy NLP library
    '''
    def __init__(self, *args, **kwargs):
        pass

    def extract(self, data_type, text, model_name):
        '''Extract NLP data for the text provided

        :arg text: (str) text body to process
        :arg data_type: (str) type of data to extract - options are:
            'sentence'
            'part-of-speech'
            'named-entity'
        :arg model_name: (str) name of spaCy model to use
        '''
        extractors = {
            'sentence': self.extract_sentence,
            'part-of-speech': self.extract_pos,
            'named-entity': self.extract_ner,
        }

        extractor = extractors.get(data_type)

        if not extractor:
            raise ValueError('"data_type" does not match a valid NLP '
                             'extractor.')

        model = self.load_model(model_name=model_name)

        results = extractor(model=model, text=text)

        return results

    def extract_sentence(self, model, text):
        '''Extract sentences from a text

        :arg model: (spaCy model) a spaCy NLP model
        :arg text: (str) text to process
        '''
        parser = model(text)
        sentences = [sentence.text for sentence in parser.sents]

        return sentences

    def extract_pos(self, model, text):
        '''Extract part-of-speech tags from a text

        :arg model: (spaCy model) a spaCy NLP model
        :arg text: (str) text to process
        '''
        document = model(text)

        pos_tokens = [
            {
                'index': token.i,
                'start_char': token.idx,
                'end_char': token.idx + len(token.text),
                'text': token.text,
                'lemma': token.lemma_,
                'pos': token.pos_,
                'pos_detail': token.tag_,
                'dependency': token.dep_,
                'shape': token.shape_,
                'parent': None if token.head.i == token.i else token.head.i,
                'children': [child.i for child in token.children],
                'is': {
                    'url': token.like_url,
                    'email': token.like_email,
                    'currency': token.is_currency,
                    'alpha': token.is_alpha,
                    'digit': token.is_digit,  # Only digits '123', '456'
                    'number': token.like_num,  # Includes '10.9', 'ten'
                    'out_vocab': token.is_oov,  # Out of vocabulary
                    'stop': token.is_stop,  # Part of a "stop list"
                    'punct': token.is_punct,
                    'left_punct': token.is_left_punct,
                    'right_punct': token.is_right_punct,
                    'space': token.is_space,
                    'bracket': token.is_bracket,
                    'quote': token.is_quote,
                },
            }
            for token in document
        ]

        return pos_tokens

    def extract_ner(self, model, text):
        '''Extract named entities from a text

        :arg model: (spaCy model) a spaCy NLP model
        :arg text: (str) text to process
        '''
        parser = model(text)

        entities = [
            {
                'text': str(entity.text),
                'start': int(entity.start_char),
                'end': int(entity.end_char),
                'label': str(entity.label_),
            }
            for entity in parser.ents
        ]

        return entities

    def load_model(self, model_name):
        '''Load a spaCy NLP model from local filesystem or AWS S3

        :arg model_name: (str) name of spaCy model to load
        '''
        model_path = os.path.join('tmp', model_name)

        # Check whether the model is already in local filesystem
        if not os.path.isdir(model_path):
            self.download_model(model_name=model_name)

        # Instantiate model
        model = spacy.load(model_path)

        return model

    def download_model(self, model_name):
        '''Download spaCy model file from AWS S3

        :arg model_name: (str) name of spaCy model to load
        '''
        print('Model not available locally, downloading from S3')

        file_name = f'{model_name}.zip'
        local_path = os.path.join('tmp', file_name)
        remote_path = os.path.join(file_name)

        s3 = boto3.resource('s3')

        s3.Bucket(c.MODEL_S3_BUCKET_NAME) \
          .download_file(remote_path, local_path)

        # Unzip the model in local filesystem
        with ZipFile(local_path, 'r') as zip_file:
            zip_file.extractall('tmp')

        # Delete the zip file to save space on the local /tmp directory
        os.remove(local_path)
