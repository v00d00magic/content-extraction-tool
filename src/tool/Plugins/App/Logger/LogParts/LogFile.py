from Objects.Object import Object
from pathlib import Path
from pydantic import Field
from Objects.Object import Object
from datetime import datetime
from enum import Enum

class LogModeEnum(Enum):
    per_day = 0
    per_startup = 1

class LogFile(Object):
    items: list = []
    mode: LogModeEnum = LogModeEnum.per_startup
    created: datetime = Field(default=lambda: datetime.now())
    filename: str = None
    path: Path = None

    def getFile(self):
        match(self.mode):
            case LogModeEnum.per_startup.value:
                filename = f"{self.created.strftime('%Y-%m-%d_%H-%M-%S')}.json"
            case LogModeEnum.per_day.value:
                filename = f"{self.created.strftime('%Y-%m-%d')}.json"

        return filename

    def open(self, storage):
        self.path = storage.dir.joinpath(self.getFile())
        if self.path.exists() == False:
            t = open(self.path, 'w', encoding='utf-8')
            t.close()

        self.stream = open(str(self.path), 'r+', encoding='utf-8')

    def add(self, log):
        self.items.append(log)

    def save(self):
        pass

    @staticmethod
    def new(storage):
        file = LogFile(
            mode = LogModeEnum.per_startup.value
        )
        file.open(storage)

        return file
