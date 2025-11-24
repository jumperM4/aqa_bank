import allure


class StepLogger:
    def log_step(self, title, func, *args, **kwargs):
        with allure.step(title):
            return func(*args, **kwargs)
