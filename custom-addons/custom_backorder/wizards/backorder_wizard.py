from odoo import models, fields, api

class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process_with_custom_options(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Backorder Confirmation',
            'res_model': 'stock.backorder.confirmation',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
            'view_id': self.env.ref('custom_backorder.backorder_wizard_view').id,
        }

    def process_create_backorder(self):
        """Create a backorder for remaining quantities in Requested (draft) status."""
        self.ensure_one()
        pickings = self.pick_ids
        backorders = pickings._create_backorder()
        for backorder in backorders:
            backorder.state = 'draft'
        return pickings._action_done()

    def process_no_backorder(self):
        """Confirm only available quantities, cancel the rest."""
        self.ensure_one()
        pickings = self.pick_ids
        for picking in pickings:
            for move in picking.move_ids:
                move.product_uom_qty = sum(move_line.quantity for move_line in move.move_line_ids)
        return pickings._action_done()