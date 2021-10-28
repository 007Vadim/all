import os
import shutil
import uuid
from datetime import datetime
from typing import List
from fastapi import FastAPI, File, UploadFile
from starlette.responses import HTMLResponse

import dir
import sql

app = FastAPI()

PATH = 'C:/Users/мфц/PycharmProjects/fastapi/data/'


@app.put("/frame/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        if file.content_type != 'image/jpeg' or len(files) > 15:
            return 'Ошибка'
    dat = datetime.today().strftime('%Y-%m-%d')
    if not os.path.exists(f'{PATH}{dat}'):
        os.makedirs(f'{PATH}{dat}')
    id_num = sql.max_id()
    for file in files:
        name = f'{PATH}{dat}/{uuid.uuid4()}.jpg'
        with open(name, 'wb+') as out_file:
            shutil.copyfileobj(file.file, out_file)
            sql.create_upload_jpg(id_num, name)
    return {"Result": "OK", "fileb_content_type": [file.content_type for file in files]}


@app.get("/frame")
async def main():
    content = """
<body>
<form action="/upload-file/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/frame/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.delete('/frame/{id_num}')
async def dele(id_num):
    for i in sql.select_jpg(id_num):
        name = i[0].split('/')[7]
        dir.del_img(name, PATH=PATH)
    return sql.del_jpg(id_num)


@app.get('/frame/{id}')
async def img(id):
    res = sql.select_jpg(id)
    return res
