from fastapi import FastAPI
from boilerpy3 import extractors
import requests

app = FastAPI()

# domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.

@app.get("/")
def home():
    return {"message": "Hello World!"}

@app.get("/get_content/")
def get_content(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36',
    }
    url_valid = uri_exists_stream(url, headers)
    if url_valid == True:
        extractor = extractors.KeepEverythingExtractor()
        try:
            doc = extractor.get_content_from_url(url)
            return {"content": doc}
        except:
            pass
    else:
        return {'msg': url_valid}

def uri_exists_stream(uri: str, headers) -> bool:
    try:
        with requests.get(uri, stream=True, headers=headers) as response:
            try:
                response.raise_for_status()
                return True
            except requests.exceptions.HTTPError as err:
                return {'err': err, 'status_code': err.response.status_code}
    except requests.exceptions.ConnectionError as err:
        return {'err': err, 'status_code': err.response.status_code}
