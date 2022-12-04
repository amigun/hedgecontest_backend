from fastapi import Depends, HTTPException

from src.db.repositories.users import UsersOperation


class Need:
    def need(self, roles: list, token: dict):
        try:
            print(f'\n\n\n{token}\n\n\n')
            print(f'\n\n\n{roles}\n\n\n')
            role = token['sub'].split(':')[1]
        except TypeError:
            print('typeerroooooooooooooooooor')
            return None

        if role in roles:
            pass
        else:
            print('eeeeeeeeeeeeelse')
            return None
