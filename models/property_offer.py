from odoo import fields, models, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class AbstractOffer(models.AbstractModel):
    _name = 'abstract.model.offer'
    _description = 'Abstract offers'

    partner_email = fields.Char(string="Email")
    partner_phone = fields.Char(string="Phone Number")


class PropertyOffer(models.Model):
    _name = 'estates.property.offer'
    _inherit = ['abstract.model.offer']
    _description = 'Estate Property Offers'

    name = fields.Char(string="Description", compute="_compute_name", store=True)
    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        default='refused'
    )
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estates.property', string="Property")
    validity = fields.Integer(string="Validity (Days)", default=7)
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline', store=True)
    creation_date = fields.Date(string="Creation Date", default=fields.Date.context_today)

    # _sql_constraints = [
    #     ('check_validity', 'CHECK(validity > 0)', 'The validity period must be positive.')
    # ]

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.property_id.name} - {rec.partner_id.name}" if rec.property_id and rec.partner_id else False

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = 0

    @api.constrains('creation_date', 'deadline')
    def _check_deadline(self):
        for rec in self:
            if rec.deadline and rec.deadline <= rec.creation_date:
                raise ValidationError(_("The deadline must be after the creation date."))

    def _validate_no_accepted_offer(self):
        if self.search_count([('property_id', '=', self.property_id.id), ('status', '=', 'accepted')]):
            raise ValidationError(_("An offer has already been accepted for this property."))

    def action_accept_offer(self):
        self._validate_no_accepted_offer()
        self.property_id.write({
            'selling_price': self.price,
            'state': 'accepted'
        })
        self.status = 'accepted'

    def action_decline_offer(self):
        self.status = 'refused'
        if all(offer.status == 'refused' for offer in self.property_id.offer_ids):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })
