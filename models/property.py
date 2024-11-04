from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = 'estates.property'
    _description = 'Estate Properties'
    color = fields.Integer(string="Color")

    name = fields.Char(string="Property Name", required=True)
    state = fields.Selection(
        [('new', 'New'),
         ('received', 'Offer Received'),
         ('accepted', 'Offer Accepted'),
         ('sold', 'Sold'),
         ('cancel', 'Cancelled')],
        default='new', string="Status")
    tag_ids = fields.Many2many('estates.property.tag', string="Property Tag")
    type_id = fields.Many2one('estates.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    dates_availability = fields.Date(string="Available From", readonly=False)
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer", compute='_compute_best_price')
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=0)
    living_area = fields.Integer(string="Living Area (sqm)", default=0)
    facades = fields.Integer(string="Facades", default=0)
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area", default=0)
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation", default='north')
    offer_ids = fields.One2many('estates.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    total_area = fields.Integer(string="Total Area")

    @api.onchange('living_area', 'garden_area')
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute=_compute_offer_count)

    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estates.property.offer'
        }

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0


class PropertyType(models.Model):
    _name = 'estates.property.type'
    _description = 'Property Type'
    name = fields.Char(string="Name", required=True)


class PropertyTags(models.Model):
    _name = 'estates.property.tag'
    _description = 'Property Tag'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
