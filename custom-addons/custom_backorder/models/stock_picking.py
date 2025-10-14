from odoo import models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        self.ensure_one()
        if not self.move_ids and not self.move_line_ids:
            return super(StockPicking, self).button_validate()

        for picking in self:
            for move in picking.move_ids:
                # Check done quantity on move lines
                done_qty = sum(move_line.quantity for move_line in move.move_line_ids)
                if done_qty < move.product_uom_qty:
                    return self.env['stock.backorder.confirmation'].create({
                        'pick_ids': [(6, 0, self.ids)],
                    }).process_with_custom_options()
        return super(StockPicking, self).button_validate()