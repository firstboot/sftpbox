# from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from starlette.responses import StreamingResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
import mimetypes

# import io
import os
import json
import time

from sshbox import SSHBoxClient
from model import *

import logging.handlers
logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler('netshell.log', when='midnight', interval=1, backupCount=7)
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(rf_handler)


app = FastAPI()


origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

tmp_path = './dtmp/'
upload_tmp_path = './utmp/'
share_path = './share/'
port = 8000

client_db = {}

# save mem, apply to small size file
# @app.post("/files/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}


@app.post("/uploadfile")
async def upload_file(
        request: Request,
        file: UploadFile = File(...)
):
    try:
        fileSize = request.headers.get('file-size')
        logger.info('fileSize: ', fileSize, type(fileSize))
        file.spool_max_size = int(fileSize)

        logger.info(file.spool_max_size)
        logger.info(file.content_type)
        f = open(upload_tmp_path + file.filename, 'wb')
        s = await file.read(file.spool_max_size)
        f.write(s)
        f.close()
        await file.close()

        uploadParams = request.headers.get('upload-params')
        uploadParamsDict = json.loads(uploadParams)

        host_ip = uploadParamsDict['hostIp']
        username = uploadParamsDict['username']
        location = uploadParamsDict['location']

        key = host_ip + username
        ssh_client = client_db[key]

        local_path = upload_tmp_path + file.filename
        remote_path = location + '/' + file.filename
        ssh_client.put(local_path, remote_path)

        os.remove(local_path)
        return {"filename": file.filename}
    except Exception as e:
        return RetCls.ret(False, str(e), [{}])


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        logger.info(tmp_path+file.filename)
        f = open(tmp_path+file.filename, 'wb')
        s = await file.read(file.spool_max_size)
        f.write(s)
        f.close()
        await file.close()
    return {"filenames": [file.filename for file in files]}


@app.post("/listFiles")
async def list_files(arg_list_files: ArgListFiles):
    try:
        key = arg_list_files.hostIp+arg_list_files.username
        ssh_client = client_db[key]
        all_files = ssh_client.get_all_files_in_remote_dir(arg_list_files.location)
        res = RetCls.ret(True, '', all_files)
        logger.info(key)
        logger.info(res)
        return res
    except Exception as e:
        return RetCls.ret(False, str(e), [{}])


@app.post("/getFile")
async def get_file(arg_get_file: ArgGetFile):
    try:
        key = arg_get_file.hostIp + arg_get_file.username
        ssh_client = client_db[key]
        pos = arg_get_file.remotePath.rfind('/')
        file_name = arg_get_file.remotePath[pos:]

        ssh_client.get_file(arg_get_file.remotePath, tmp_path)

        path = tmp_path + file_name
        path = path.replace('//', '/')
        logger.info('getFile: ', path)
        mt = mimetypes.guess_type(path)[0]
        logger.info('media_type = ', mt)

        # f = open(path, 'rb')
        # res = StreamingResponse(io.BytesIO(f.read()), media_type=mt)
        # f.close()
        # os.remove(path)
        res = FileResponse(path, media_type=mt)
        return res

    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/getShare")
async def get_share(arg_get_file: ArgGetFile):
    try:
        key = arg_get_file.hostIp + arg_get_file.username
        ssh_client = client_db[key]
        pos = arg_get_file.remotePath.rfind('/')
        file_name = arg_get_file.remotePath[pos:]
        ssh_client.get_file(arg_get_file.remotePath, share_path)
        return RetCls.ret(True, {"share": "/share"+file_name}, {})

    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/removeShareFile")
async def remove_share_file(arg_remove: ArgPath):
    try:
        logger.info(arg_remove)
        os.remove(arg_remove.path)
        return RetCls.ret(True, '', {})
    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/getShareFiles")
async def get_share_files():
    try:
        rets = []
        for item in os.listdir(share_path):
            path = share_path + item
            file_item = {}
            file_item['name'] = item
            file_item['path'] = '/share/' + item
            file_item['size'] = os.path.getsize(path)
            # file latest modified time
            file_item['mTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
            file_item['type'] = 'file'
            rets.append(file_item)
        return RetCls.ret(True, '', rets)
    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/getHistory")
async def get_history(arg: ArgPath):
    try:
        key = arg.hostIp + arg.username
        ssh_client = client_db[key]
        rets = ssh_client.get_history()
        return RetCls.ret(True, '', rets)
    except Exception as e:
        return RetCls.ret(False, str(e), [])


@app.post("/getDf")
async def get_df(arg: ArgPath):
    try:
        key = arg.hostIp + arg.username
        ssh_client = client_db[key]
        rets = ssh_client.get_df()
        return RetCls.ret(True, '', rets)
    except Exception as e:
        return RetCls.ret(False, str(e), [])


@app.post("/getFileAfter")
async def get_file_after(arg_get_file_after: ArgGetFileAfter):
    try:
        file_name = arg_get_file_after.fileName
        path = tmp_path + file_name
        path = path.replace('//', '/')
        os.remove(path)
        return RetCls.ret(True, '', {'fileName': path})
    except Exception as e:
        return RetCls.ret(False, str(e), {'fileName': path})


@app.post("/rename")
async def rename(arg_rename: ArgOpNp):
    try:
        key = arg_rename.hostIp+arg_rename.username
        ssh_client = client_db[key]
        ssh_client.rename(arg_rename.oldPath, arg_rename.newPath)
        return RetCls.ret(True, '', {})
    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/copy")
async def copy(arg_copy: ArgOpNp):
    try:
        key = arg_copy.hostIp+arg_copy.username
        ssh_client = client_db[key]
        ssh_client.copy(arg_copy.oldPath, arg_copy.newPath)
        return RetCls.ret(True, '', {})
    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/remove")
async def remove(arg_remove: ArgPath):
    try:
        key = arg_remove.hostIp + arg_remove.username
        ssh_client = client_db[key]
        ssh_client.remove(arg_remove.path)
        return RetCls.ret(True, '', {})
    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/mkdir")
async def mkdir(arg_mkdir: ArgPath):
    try:
        key = arg_mkdir.hostIp + arg_mkdir.username
        ssh_client = client_db[key]
        ssh_client.mkdir(arg_mkdir.path)
        return RetCls.ret(True, '', {})
    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.post("/login")
async def login(client: Client):
    try:
        pos = client.hostIp.find(':')
        if pos >= 0:
            ip = client.hostIp[:pos]
            port = int(client.hostIp[pos+1:])
        else:
            ip = client.hostIp
            port = 22
        logger.info('ip-port:', ip, port)
        ssh_client = SSHBoxClient(ip=ip, port=port, username=client.username, password=client.password)
        key = client.hostIp+client.username
        client_db[key] = ssh_client
        logger.info("login ..... ")
        data = {'key': key, 'hostIp': client.hostIp, 'username': client.username}
        return RetCls.ret(True, '', data)
    except Exception as e:
        return RetCls.ret(False, str(e), {})


@app.get("/")
async def main():
    return RedirectResponse("/static/index.html")


def load_config(config_path):

    f = open(config_path, 'r')
    config_text = f.read()
    # logger.info(config_text)
    f.close()

    config_dt = json.loads(config_text)
    tmp_path = config_dt['tmp_path']
    upload_tmp_path = config_dt['upload_tmp_path']
    share_path = config_dt['share_path']
    origins = config_dt['origins']
    port = int(config_dt['port'])
    logger.info('tmp_path: '+tmp_path)
    logger.info('upload_tmp_path: '+upload_tmp_path)
    logger.info('share_path: '+share_path)
    logger.info('port: '+str(port))
    logger.info('origins: '+str(origins))


if __name__ == '__main__':
    import uvicorn

    load_config('./config.json')
    logger.info("")

    logger.info('tmp_path: '+str(os.path.exists(tmp_path)))
    logger.info('upload_tmp_path: '+str(os.path.exists(upload_tmp_path)))
    logger.info('share_path: '+str(os.path.exists(share_path)))

    if os.path.exists(tmp_path) is False:
        os.mkdir(tmp_path)
        logger.info('tmp_path created')

    if os.path.exists(upload_tmp_path) is False:
        os.mkdir(upload_tmp_path)
        logger.info('upload_tmp_path created')

    if os.path.exists(share_path) is False:
        os.mkdir(share_path)
        logger.info('share_path created')

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/share", StaticFiles(directory="share"), name="share")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        # allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="0.0.0.0", port=port)
