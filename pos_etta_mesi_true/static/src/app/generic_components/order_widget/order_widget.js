/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(OrderWidget.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    getVoidedItems() {
        return [];
    },
    get orderlines() {
        const order = this.pos?.get_order();
        if (!order) {
            console.warn("No current order found");
            return [];
        }

        const lines = order.get_orderlines?.();
        if (!Array.isArray(lines)) {
            console.warn("Orderlines not available or invalid");
            return [];
        }

        return lines;
    },
    get product_total() {
        let order = this.pos.get_order();
        var orderlines = order.get_orderlines();
        return orderlines.length;
    },
});