import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Example extends Component {
    static template = "my_module.Example";
}

registry.category("main_components").add("my_module.Example", Example); 