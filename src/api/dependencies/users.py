from fastapi import Depends, HTTPException

from src.db.repositories.users import UsersOperation


class Need:
    def need(self, roles: list, token: dict):
        try:
            role = token['sub'].split(':')[1]
        except TypeError:
            return None

        if role in roles:
            pass
        else:
            return None
