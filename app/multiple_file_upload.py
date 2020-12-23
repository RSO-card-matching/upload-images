from typing import List, Optional
import base64
from PIL import Image
import requests

from fastapi import FastAPI, File, UploadFile, Header, Request
from fastapi.responses import HTMLResponse
from starlette.datastructures import URL
from starlette.responses import RedirectResponse

app = FastAPI()

{
    "Version": "13.1.0",
    "Name": "s-ul",
    "DestinationType": "ImageUploader, TextUploader, FileUploader",
    "RequestType": "POST",
    "RequestURL": "https://s-ul.eu/api/v1/upload",
    "Arguments": {
        "wizard": "true",
        "key": "5fBfpmtiREySkwl5t1aFSwSKdDPD6O7E1IhohWQOtW6LBWPfZBBjwbvexmes"
    },
    "FileFormName": "file",
    "URL": "$json:url$",
    "ThumbnailURL": "$json:url$?thumb=1",
    "DeletionURL": "https://s-ul.eu/delete.php?key=5fBfpmtiREySkwl5t1aFSwSKdDPD6O7E1IhohWQOtW6LBWPfZBBjwbvexmes&file=$json:filename$"
}

fake_items_db = [{"wizard": "true"}, {"key": "5fBfpmtiREySkwl5t1aFSwSKdDPD6O7E1IhohWQOtW6LBWPfZBBjwbvexmes"}]

@app.post("/data/")
async def api_data(request: Request):
    params = str(request.query_params)
    file = open('Skupaj.jpg')
    params = str("wizard:true, key:5fBfpmtiREySkwl5t1aFSwSKdDPD6O7E1IhohWQOtW6LBWPfZBBjwbvexmes, file:"+file)
    url = f'https://s-ul.eu/api/v1/upload/{params}'
    response = RedirectResponse(url=url)
    return response

@app.post("/create_file/")
async def create_file(files2: List[UploadFile] = File(...)):
    params = str("wizard:true, key:5fBfpmtiREySkwl5t1aFSwSKdDPD6O7E1IhohWQOtW6LBWPfZBBjwbvexmes")
    url = f'https://s-ul.eu/api/v1/upload/{params}'
    r = requests.post(url, files=files2)
    r.text
    return r.text


@app.get("/items/{item_id}")
async def read_item(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}

@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"wizard": "true", "key": "5fBfpmtiREySkwl5t1aFSwSKdDPD6O7E1IhohWQOtW6LBWPfZBBjwbvexmes"}


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>

<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" accept="image/*" multiple>
<input type="submit">
</form>
<form action="/create_file/" enctype="multipart/form-data" method="post">
<input name="files" type="file" accept="image/*" multiple>
<input type="submit" value="test">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" accept="image/*" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)