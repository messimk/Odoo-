/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
async setup() {
await super.setup(...arguments);
//setInteval here for the polling
console.log("Setting up the store");
}
});