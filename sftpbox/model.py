from pydantic import BaseModel


class Client(BaseModel):
    hostIp: str
    username: str
    password: str


class ArgListFiles(BaseModel):
    hostIp: str
    username: str
    location: str


class ArgGetFile(BaseModel):
    hostIp: str
    username: str
    remotePath: str


class ArgGetFileAfter(BaseModel):
    fileName: str


class ArgOpNp(BaseModel):
    hostIp: str
    username: str
    oldPath: str
    newPath: str


class ArgPath(BaseModel):
    hostIp: str
    username: str
    path: str


class ArgUploadFile(BaseModel):
    hostIp: str
    username: str
    location: str


class RetCls(object):
    @classmethod
    def ret(cls, status=False, msg='', data={}):
        return {
            'status': status,
            'msg': msg,
            'data': data
        }
