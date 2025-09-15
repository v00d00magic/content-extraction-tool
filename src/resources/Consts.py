from pathlib import Path
import platform, os

consts = {}

# OS
consts["os.name"] = platform.system()
consts["pc.name"] = os.getenv("COMPUTERNAME", "NoName-PC")
consts["pc.user"] = os.getlogin()
consts["pc.fullname"] = consts["pc.name"] + ", " + consts["pc.user"]

# Runtime
consts["cwd"] = Path(os.getcwd())

# Config
consts["config.hidden"] = 1
consts["config.hidden_values_spaces"] = ["db.", "web."]

# Args
consts["arguments.forbidden"] = ["i", "name", "confirm"]
