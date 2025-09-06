import Controller from "./Controller.js"
import router from "../router.js"
import api from "../api/api.js"
import Executable from "../models/Executables/Executable.js"

class ExecutableController extends Controller {
    async executable_page(container) {
        const executable_name = router.url.getParam("title")
        const executable = await Executable.byName(executable_name)

        container.title(executable.extended_name)
        container.set(`
            <p>${executable.name}</p>
            <p>${executable.description}</p>
            <p><b>Submodules</b></p><br>
            <div style="display:flex;flex-direction:column" id="submodules"></div>
            <p><b>Execute</b></p><br>
            <div style="display:flex;flex-direction:column" id="execute"></div>
            <div id="json"></div>
        `)
        executable.variants.forEach(item => {
            container.node.find("#submodules").append(`<a href="#executable?title=${item.extended_name}">${item.extended_name}</a>`)
        })

        const args = new class {
            _items = []
            print(args, _container) {
                args.forEach(item => {
                    this._items.push(item)
                    item.render(_container)
                })
            }

            values() {
                const _out = {}
                this._items.forEach(item => {
                    _out[item.name] = item.collect()
                })

                return _out
            }
        }

        args.print(executable.args, container.node.find("#execute"))

        container.node.find("#execute").append(`<input id="execute_button" type="button" value="Execute">`)
        container.node.find("#execute #execute_button").on("click", async (e) => {
            const values = args.values()

            values["i"] = "Executables.Execute"
            values["executable"] = executable.extended_name
            const res = await api.act(values)

            const jsonViewer = document.createElement("andypf-json-viewer")

            jsonViewer.data = res
            jsonViewer.expanded = true
            jsonViewer.indent = 4
            jsonViewer.expanded = 4
            jsonViewer.showDataTypes = false
            jsonViewer.showSize = false

            container.node.find("#json").append(jsonViewer)
        })
    }

    async executables_list(container) {
        container.title("Executables list")
        container.set(`
            <div id="executables">
                <div style="display:flex;flex-direction:column" id="executables_list"></div>
            </div>
        `)

        const items = await Executable.all()
        items.forEach(item => {
            container.node.find("#executables_list").append(`
                <a href="#executable?title=${item.extended_name}">${item.extended_name}</a>    
            `)
        })
    }
}

export default ExecutableController
