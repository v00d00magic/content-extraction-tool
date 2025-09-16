from executables.ExecutableCall import ExecutableCall
from executables.list.Executables.Execute import Implementation as Execute
from utils.MainUtils import dump_json
from app.App import app

app.context = "cli"

async def call():
    app.setup()

    assert "i" in app.argv, "pass the name of act as --i"
    is_silent = 'silent' in app.argv

    call = ExecutableCall(executable=Execute)
    call.passArgs(app.argv)

    output = await call.run_asyncely()

    if is_silent == False:
        print(dump_json(output.display(), indent=4))
