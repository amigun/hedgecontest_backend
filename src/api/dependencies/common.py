from fastapi import Depends

from src.db.repositories.steps import StepsOperation


class Timing:
    def timing(self, step: str, steps_operation: StepsOperation = Depends()):
        current_status = steps_operation.get_status()

        if current_status != step:
            return None
        else:
            return current_status
