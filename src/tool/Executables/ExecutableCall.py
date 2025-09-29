from Executables.Templates.Executable import Executable
from Executables.Responses.Response import Response
from Utils.Hookable import Hookable
from Utils.Data.JSON import JSON
from App import app
import asyncio

class ProgressMessage():
    def __init__(self, message, percentage, index):
        self.message = message
        self.percentage = percentage
        self.index = index

class ExecutableCall(Hookable):
    section_name = ["Executables", "ExecutableCall"]
    events = ["run", "progress"]

    def __init__(self, index = None, executable: Executable = None):
        """index (set as None): defined index of class

        executable: script class
        """
        super().__init__()

        self.index = index
        if self.index == None:
            self.index = app.executable_index.getIndex()

        self._executable_class = executable
        self.executable = executable()
        self.executable.defineWrapper(self)
        self.linking_queue = []
        self.collections = []

        def _run_hook():
            self.log(f"Executed {self.executable.getName()}", section = self.section_name)

        self.add_hook("run", _run_hook)
        # self.add_hook("progress", _progress_hook)

    def passArgs(self, args = {}):
        self._orig_args = args
        self.log(f"Executable {self.executable.getName()}: set args {JSON(self._orig_args).dump()}", section = self.section_name)

        decls = self.executable.comparerShortcut(None, self._orig_args)

        self.args = decls.dict()

    def getResult(self):
        return self.executable.getResult()

    # Running

    def run_threaded(self):
        asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: asyncio.run(self.run_asyncely()) 
        )

    async def run_asyncely(self):
        return await self._execute()

    async def _execute(self):
        self.trigger("run")

        try:
            self.log(f"Calling execute() with args: {JSON(self.args.__dict__()).dump()}", section = self.section_name)
        except:
            self.log(f"Calling execute() with args: display error", section = self.section_name)

        return Response.convert(await self.executable.execute(self.args))

    def getCollections(self):
        cols = self.executable.variable("collections")
        if cols == None:
            return []

        return cols

    # Progress

    def notifyAboutProgress(self, message, percentage: float = 0.0):
        _message = ProgressMessage(message, percentage, self.index)
        self.trigger("progress", message=_message)

    # Log

    def log(self, *args, **kwargs):
        kwargs["id_prefix"] = "ExecutableCall->" + str(self.index)
        return app.logger.log(*args, **kwargs)

    # Others

    def dump(self):
        from DB.Models.Instances.ArgumentsDump import ArgumentsDump

        dump = ArgumentsDump()
        dump.executable = self.executable.getName()

        _data = {}
        for key, val in self.args.items():
            _data[key] = str(val)

        dump.data = JSON(_data).dump()
        dump.save()

        self.log(f"Dumped {self.executable.getName()}, id {dump.id}", section = self.section_name)
