from fastapi import FastAPI
from boilerpy3 import extractors

app = FastAPI()

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.


@app.get("/")
def home():
    return {"message":"Hello TutLinks.com"}

@app.get("/get_content")
def get_content(url):
    extractor = extractors.LargestContentExtractor("https://www.whitebox.eu")
    doc = extractor.get_content_from_url(url)

    return {"content": doc}
