import Model from "../Model.js";

class Argument extends Model {
    static rec(data) {
        if (subtypes[data.type]) {
            return new subtypes[data.type](data)
        }

        return new Argument(data)
    }

    render(container) {
        this.node = this.renderUmbrella()
        container.append(this.node)
        this.events()

        return this.node
    }

    events() {
        return
    }

    renderUmbrella() {
        return u(`
            <div style="display: flex">
                ${this.name != null ? `<b>${this.name}</b>` : ""}
                <input style="width:100%" type="text" value="${this.default ?? ""}">
            </div>
        `)
    }

    collect() {
        const got_value = this.node.find("input").nodes[0].value
        if (got_value == "") {
            return null
        }

        return got_value
    }

    focus() {
        return
    }

    get current_value() {
        if (this.data.current) {
            return this.data.current
        }

        return this.default
    }

    get default() {
        return this.data.default
    }

    get name() {
        return this.data.name
    }
}

export const subtypes = {
    "StringArgument": class StringArgument extends Argument {},
    "CsvArgument": class CsvArgument extends Argument {
        renderUmbrella() {
            this.subs = []
            this._default = (this.data['default'] ?? this.data.default) ?? []

            return u(`
                <div style="display: flex">
                    ${this.name != null ? `<b>${this.name}</b>` : ""}
                    <div class="csv_argument">
                        <div style="gap: 7px;" class="column wide _items"></div>
                        <div class="flex" style="gap: 7px;">
                            <input type="button" class="fit act_btn _add_icon" value="+">
                            <input type="button" class="fit act_btn _rem_icon" value="-">
                        </div>
                    </div>
                </div>
            `)
        }

        collect() {
            const out = []
            this.subs.forEach(item => {
                out.push(item.collect())
            })

            if (out.length == 0) {
                return null
            }

            return out
        }

        events() {
            const addItem = (preset) => {
                const orig_arg = Argument.rec(this.data.orig)
                if (preset) {
                    orig_arg.data.default = preset
                }

                orig_arg.render(this.node.find(".csv_argument ._items"))
                orig_arg.focus()

                this.subs.push(orig_arg)
            }

            const removeItem = (subparam) => {
                subparam.node.remove()
                this.subs = this.subs.filter(item => item !== subparam)

                const prev_node = this.subs[this.subs.length - 1]
                if (prev_node) {
                    prev_node.node.nodes[0].focus()
                }
            }

            if (!Array.isArray(this._default)) {
                this._default = [this._default]
            }

            this._default.forEach(item => {
                addItem(item)
            })

            this.node.on('click', '._add_icon', (e) => {
                addItem('')
            })

            this.node.on('click', '._rem_icon', (e) => {
                if (this.subs.length > 0) {
                    removeItem(this.subs[this.subs.length - 1])
                }
            })
        }
    },
    "BooleanArgument": class BooleanArgument extends Argument {
        renderUmbrella() {
            return u(`
                <div style="display: flex">
                    ${this.name != null ? `<b>${this.name}</b>` : ""}
                    <input type="checkbox" ${this.default == true ? "checked" : ""}>
                </div>
            `)
        }

        collect() {
            return this.node.find("input").nodes[0].checked == true
        }
    },
    "IntArgument": class IntArgument extends Argument {
        renderUmbrella() {
            return u(`
                <div style="display: flex">
                    ${this.name != null ? `<b>${this.name}</b>` : ""}
                    <input type="number" value="${this.default}">
                </div>
            `)
        }

        collect() {
            const got = Number(this.node.find("input").nodes[0].value)
            if (got == 0) {
                return null
            }

            return got
        }
    }
}

export default Argument
