import { ws } from "../ws.js"

export const api = new class {
    async act(params = {}, outer_params = {}) {
        try {
            const res = await ws.method(params)

            console.log("API: ", params["i"], params, res)

            return res
        } catch(e) {
            throw e
        }
    }
}

export default api
