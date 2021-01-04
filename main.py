from fastapi import FastAPI
from boilerpy3 import extractors
from cleantext import clean
from validator_collection import validators, errors
import requests
import spacy
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'
}

app = FastAPI()


# domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.

@app.get("/")
def home():
    return {"message": "Hello World!"}


@app.get("/get_content/")
def get_content(url: str):
    url_spelling = validate_url(url)
    if url_spelling == True:
        url_valid = uri_exists_stream(url)
        if url_valid == True:
            extractor = extractors.KeepEverythingExtractor()
            try:
                doc = extractor.get_content_from_url(url)
                doc = normalize_text(doc)
                return {"content": doc}
            except:
                pass
        else:
            return {'msg': url_valid}
    else:
        return {'msg': {'status_code': 'malformed url'}}


def uri_exists_stream(uri: str):
    try:
        with requests.get(uri, stream=True, headers=HEADERS) as response:
            try:
                response.raise_for_status()
                return True
            except requests.exceptions.HTTPError as err:
                return {'err': err,
                        'status_code': err.response.status_code,
                        'reason': err.response.reason}
    except requests.exceptions.ConnectionError as err:
        return {'err': err,
                'status_code': err.response.status_code,
                'reason': err.response.reason}


def normalize_text(doc):
    doc = clean(doc, lower=False, no_line_breaks=True)
    return doc


@app.get("/validate_url/")
def validate_url(url: str):
    try:
        value = validators.url(url)
        return True
    except errors.InvalidURLError as err:
        return False

@app.get("/get_entities/")
def get_entities(url: str):
    validated_url = validate_url(url)
    if validated_url == True:
        validated_url = uri_exists_stream(url)
        if validated_url == True:
            nlp = spacy.load("de_core_news_sm")
            extractor = extractors.LargestContentExtractor()
            try:
                doc = extractor.get_content_from_url(url)
                doc = nlp(doc)
                entities = [str(ent) for ent in doc.ents]
                return json.dumps(entities)
            except:
                pass
        else:
            return {'msg': validated_url}
    else:
        return {'msg': {'status_code': 'malformed url'}}

