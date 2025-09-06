import Config from "./models/App/Config.js"
import router from "./router.js"
import CommonNavigation from "./ui/CommonNavigation.js"
import Container from "./ui/Container.js"
import Executable from "./models/Executables/Executable.js"

export const app = new class {
    floats = []
    messageboxes = []

    template() {
        return `
            <div id="page">
                <div id="tabs">
                    <div id="items"></div>
                </div>
                <div id="header">
                    <b><a href="#">Extraction tool</a></b>
                </div>
                <div id="content">
                    <div id="content_containment"></div>
                </div>
            </div>
        `
    }

    async _constructor() {
        u('#app').html(this.template())

        this.config = new Config()
        this.executables = await Executable.all()
        await this.config.get_items()

        const navigation = new CommonNavigation()

        this.content = new Container('#app #content #content_containment', true, {
            "new_tab": (tab) => {
                navigation.addTab(tab)
            },
            "close_tab": (tab) => {
                navigation.removeTab(tab)
            },
            "title_change": (tab) => {
                navigation.setTabTitle(tab)
            },
            "tab_focus": (tab) => {
                navigation.focusTab(tab)
            }
        })
    }
}

window.addEventListener("DOMContentLoaded", async () => {
    await app._constructor()

    console.log(router)
    window.addEventListener("hashchange", async (event) => {
        console.log(event)
        await router.route(event.newURL)
    })

    await router.route(location.href)
})

export default app
