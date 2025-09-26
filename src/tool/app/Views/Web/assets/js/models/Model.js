class Model {
    view_model = null

    constructor(data) {
        this.data = data
    }

    static fromArray(arr) {
        const f = []
        arr.forEach(el => {
            f.push(new this(el))
        })

        return f
    }

    render(container) {
        const vm = this.view_model(container, this)
        return vm.render()
    }

    get_documentation(key, fallback, fallback_lang = "en_US") {
        if (!key) {
            return fallback
        }

        const res = key[fallback_lang]

        return res ?? fallback
    }
}

export default Model
