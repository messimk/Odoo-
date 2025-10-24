/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { CashOpeningPopup } from "@point_of_sale/app/store/cash_opening_popup/cash_opening_popup";

patch(CashOpeningPopup.prototype, {
    async confirm() {
        console.log("🔄 Running fiscal sync before session opening...");
        // Run polling first to check for any pending fiscal numbers
        if (this.pos.startFsPolling) {
            await this.pos.startFsPolling('session_open'); // Run sync once before session opens
        }
        
        // Then proceed with original confirm logic
        return super.confirm(...arguments);
    }
});