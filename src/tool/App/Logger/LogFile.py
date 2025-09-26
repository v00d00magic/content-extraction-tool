from datetime import datetime

class LogFile():
    MODE_PER_DAY = 0
    MODE_PER_STARTUP = 1

    def __init__(self):
        self.items = []

    def create(self, write_mode, storage):
        now = datetime.now()
        filename = ""

        match(write_mode):
            case self.MODE_PER_STARTUP:
                filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"
            case self.MODE_PER_DAY:
                filename = f"{now.strftime('%Y-%m-%d')}.json"

        self.path = storage.dir.joinpath(filename)
        if self.path.exists() == False:
            _not_exists = open(self.path, 'w', encoding='utf-8')
            _not_exists.close()

        self.stream = open(str(self.path), 'r+', encoding='utf-8')

    def add(self, log):
        self.items.append(log)

    def save(self):
        pass
