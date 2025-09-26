import api from "../../api/api.js"
import Model from "../Model.js"
import Argument from "../Arguments/Argument.js"

class Config extends Model {
    async get_items() {
        this.data = await api.act({
            "i": "App.Config.Receive",
        }, false)
        this.data = this.data.result
    }

    static categories_from_args(args) {
        const all_categories = []

        args.forEach(item => {
            const name = item.name
            const cats = name.split(".")

            all_categories.push(cats[0])
        })

        return new Set(all_categories)
    }

    static async update(new_data) {
        return await api.act({
            "i": "App.Config.Update",
            "values": JSON.stringify(new_data)
        }, false).result
    }

    static async update_env(new_data) {
        return await api.act({
            "i": "App.Env.Update",
            "values": JSON.stringify(new_data)
        }, false).result
    }

    get items() {
        const output = []
        this.data.forEach(item => {
            output.push(Argument.rec(item))
        })

        return output
    }

    option(title) {
        let res = null
        this.items.forEach(item => {
            if (item.name == title) {
                res = item.current_value
            }
        })

        return res
    }
}

export default Config
