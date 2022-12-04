import datetime
import hashlib

from fastapi import APIRouter, UploadFile, Depends, File, status
from starlette.responses import FileResponse

from src.db.repositories.files import FilesOperation

router = APIRouter()


### TODO: add volume into docker
@router.post('/upload_file', status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile = File(...), files_operation: FilesOperation = Depends()):
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


@router.get('/download_file')
def download_file(filename: str):
    try:
        return FileResponse(path=f'files/{filename}')
    except:
        pass
