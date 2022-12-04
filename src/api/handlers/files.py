import datetime
import hashlib

from fastapi import APIRouter, UploadFile, Depends, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from starlette.responses import FileResponse

from src.api.dependencies.users import Need
from src.db.repositories.files import FilesOperation

router = APIRouter()


### TODO: add volume into docker
@router.post('/upload_file', status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile = File(...), files_operation: FilesOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['user', 'expert', 'admin'], authorize.get_raw_jwt()):
        try:
            new_filename = hashlib.md5(file.file.read()).hexdigest() + str(int(datetime.datetime.now().timestamp())) + file.filename
            file.file.seek(0)
            with open(f'files/{new_filename}', 'wb') as f:
                while True:
                    contents = file.file.read(2 ** 20)
                    print(contents)
                    if not contents:
                        break
                    f.write(contents)

            if files_operation.get_file(file.filename):
                return {'result': 'Такой файл уже существует'}
            else:
                file_id = files_operation.add_file(new_filename)

        except Exception as e:
            print(e)
            return {'result': 'Ошибка при загрузке файла'}
        finally:
            file.file.close()

        return {'filename': new_filename}
    else:
        return HTTPException(status_code=401, detail='Нету прав доступа')


@router.get('/download_file')
def download_file(filename: str):
    try:
        return FileResponse(path=f'files/{filename}')
    except:
        pass
