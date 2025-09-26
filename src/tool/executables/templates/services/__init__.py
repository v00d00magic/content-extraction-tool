from app.App import logger
from executables.templates.Executable import Executable
from app.Logger.LogSection import LogSection

class EndOfCycleException(Exception):
    pass

class Service(Executable):
    self_name = "Service"

    def __init__(self):
        self.config = {}
        self.interval = 10
        self.current_iteration = 0
        self.max_iterations = -1
        self.service_object = None
        self.is_stopped = False

    async def iteration(self, i):
        self.current_iteration = self.current_iteration + 1

        _symbol = '∞'
        if self.max_iterations > 0:
            if self.current_iterator > self.max_iterations:
                raise EndOfCycleException("Reached the end of cycle")

            _symbol = self.max_iterations

        self.log(message=f"Making run {self.current_iteration}/{_symbol}", section="Service")

        return await self.execute(i)

    def stop(self):
        self.is_stopped = True

    def implementation(self, args = {}):
        pass

    def terminate(self):
        exit(-1)
