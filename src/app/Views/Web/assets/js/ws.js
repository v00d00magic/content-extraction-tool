import { ApiError } from "./api/ApiError.js"

class WSEvent {
    constructor(type, index, payload) {
        this.type = type
        this.index = index
        this.payload = payload
    }

    toJson() {
        return JSON.stringify({"type": this.type, "event_index": this.index, "payload": this.payload})
    }
}

export const ws = new class {
    ws = null
    callback_dictionary = {}
    events_count = 1

    constructor() {
        this.connect()
    }

    connect() {
        this.ws = new WebSocket(`ws://${location.host}/ws`)
        this.ws.onopen = () => {
            const ev = new WSEvent("ping", 0)
            this.ws.send(ev.toJson())
        }

        this.ws.onmessage = (message) => {
            const ws_message = JSON.parse(message.data)
            const ev = new WSEvent(ws_message.type, ws_message.event_index, ws_message.payload)
            const callback = this.callback_dictionary[ev.index]

            switch(ev.type) {
                case "log":
                    console.log(`Logger message: `, ev.payload['result'])

                    break
                case "act":
                    if (callback) {
                        if (ev.payload.error) {
                            callback.reject(new ApiError(ev.payload.error.message, ev.payload.error.exception_name, ev.payload.error.status_code))
                        } else {
                            callback.resolve(ev.payload)
                        }
                    }
            }
        }

        this.ws.onerror = (error) => {}
    }

    increment_index() {
        this.events_count += 1
    }

    async method(params, attempt = 0) {
        if (attempt > 5) {
            return null
        }

        if (!this.ws.readyState) {
            await new Promise(resolve => setTimeout(resolve, 100))
            return await this.method(params, attempt + 1)
        }

        return new Promise((resolve, reject) => {
            const event = new WSEvent("act", this.events_count, params)
            this.callback_dictionary[event.index] = {resolve, reject}

            try {
                this.ws.send(event.toJson())
                this.increment_index()
            } catch(err) {
                reject(err)
            }
        })
    }
}

export default ws
