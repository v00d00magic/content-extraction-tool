import Controller from "./Controller.js"
import routes from "../resources/routes.js"

class AboutController extends Controller {
    async main(container) {
        container.title("Index")
        container.set(`
            <div>v0.0</div>
                
            <div id="routes">
                <div style="display:flex;flex-direction:column" id="routes_list"></div>
            </div>
        `)

        routes.forEach(el => {
            container.node.find("#routes #routes_list").append(`
                <a href="#${el.route}">${el.route}</a>
            `)
        })
    }

    async not_found(container) {
        container.title("Not found route")
        container.set(`not_found`)
    }
}

export default AboutController
