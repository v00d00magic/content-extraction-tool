from db.Models.Instances.ArgumentsDump import ArgumentsDump
from utils.MainUtils import dump_json
from app.App import app, logger
import asyncio

class ExecutableCall():
    '''
    Wrapper of executable
    '''
    def __init__(self, index = None, executable = None):
        self.index = index
        if self.index == None:
            self.index = app.getIndex()

        self._executable_class = executable
        self.executable = executable()
        self.executable.defineWrapper(self)
        self._run_hook()

    def passArgs(self, args = {}):
        self._orig_args = args

        decls = self.executable.comparer_shortcut(None, self._orig_args)

        self.args = decls.dict()

    def _run_hook(self):
        logger.log(f"Executed {self.executable.full_name()}", section=logger.SECTION_EXECUTABLES, id=self.index)

    def run_threaded(self):
        asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: asyncio.run(self.run_asyncely()) 
        )

    async def run_asyncely(self):
        return await self.executable.execute(self.args)

    def dump(self):
        dump = ArgumentsDump()
        dump.executable = self.executable.full_name()
        dump.data = dump_json(self.args)
        dump.save()

        logger.log(f"Dumped {self.executable.full_name()}, id {dump.id}", section=logger.SECTION_EXECUTABLES, id=self.index)
