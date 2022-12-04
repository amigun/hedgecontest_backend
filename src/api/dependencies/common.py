from src.db.repositories.steps import StepsOperation


class Timing:
    def timing(self, step: str):
        current_status = StepsOperation().get_status()

        if current_status != step:
            return None
        else:
            return current_status
