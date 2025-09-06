import Model from "../Model.js"
import Argument from "../Arguments/Argument.js"
import api from "../../api/api.js"

class Executable extends Model {
    static async byName(class_name) {
        const resp = await api.act({
            'i': "Executables.Describe",
            'class': class_name
        })

        return new Executable(resp.result)
    }
    
    static async all() {
        const resp = await api.act({
            'i': "Executables.List",
        })
        const output = []
        resp.result.forEach(item => {
            output.push(new Executable(item))
        })

        return output
    }

    get extended_name() {
        return `${this.data.class}`
    }

    get name() {
        return this.get_documentation(this.data.docs['name'], this.data.name)
    }

    get description() {
        return this.get_documentation(this.data.docs['definition'], "No description")
    }

    get args() {
        const args = this.data.args
        if (!args) {
            return []
        }

        const output = []
        args.forEach(item => {
            output.push(Argument.rec(item))
        })

        return output
    }

    get variants() {
        const variants = this.data.variants
        if (!variants) {
            return []
        }

        const output = []
        variants.forEach(item => {
            output.push(new Executable(item))
        })

        return output
    }
}

export default Executable
