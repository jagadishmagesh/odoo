from odoo import api, models, fields, tools, _


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    amount_un = fields.Text(string="Amount")
    product_id = fields.Many2one('purchase.order.line')
    amount_untaxed = fields.Monetary(string='Total Amount', related='product_id.amount_untaxed')
    order_line = fields.Many2one('purchase.order')
    product_id = fields.Many2one('purchase.order.line')
    name = fields.Many2one('purchase.order.line')
    product_qty = fields.Many2one('purchase.order.line')
    currency_id = fields.Many2one('res.currency', string='Currency')
    price_unit = fields.Many2one('purchase.order.line')
    values = fields.Monetary('TTTTotal Value', readonly=True, compute = 'compute_stock_value')

    def compute_stock_value(self):
        val = self.env['purchase.order.line'].sudo().search([
            # ('product_id', '=', self.product_id.id),
            ('name', '=', self.name),
            ('product_qty', '=', self.product_qty),
            ('price_unit', '=', self.price_unit),
        ])
        for rec in self:
            for res in val:
                rec.values = res.price_unit * res.product_qty
                return rec.values

    # @api.depends('price_unit', 'name')
    # def compute_stock_value(self):
    #     for rec in self:
    #         rec.values = rec.price_unit * rec.product_qty
    #         return rec.values
