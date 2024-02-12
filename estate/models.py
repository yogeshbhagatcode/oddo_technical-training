from datetime import timedelta
from odoo import models, fields, api

class TestModel(models.Model):
    _name = 'test_model'
    _description = "Test Model"

    name = fields.Char()


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = "Estate Property model"

    name = fields.Char(required=True)
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text()
    state = fields.Selection(string='State', 
            selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Select state", required=True, default='new')
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    salesman = fields.Many2one("res.users", string="Salesman", default= lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate_property_tag", string="Tag IDs")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Select type")
    total_area = fields.Integer(compute = "_compute_total_area")
    offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offers")
    best_price = fields.Integer(compute='_compute_best_price')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            best_price = max(record.offer_ids.mapped('price'), default=0)
            record.best_price = best_price
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        elif not self.garden:
            self.garden_area = 0
            self.garden_orientation = None



class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = "Estate Property Type model"

    name = fields.Char(required=True)


class EstatePropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = "Estate Property Tag model"

    name = fields.Char(required=True)


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = "Estate Property Offer model"
    _rec_name = 'price'

    price = fields.Float()
    status = fields.Selection(string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date)
                record.date_deadline = (create_date + timedelta(days=record.validity)).date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = fields.Datetime.from_string(record.create_date)
                record.validity = (fields.Datetime.from_string(record.date_deadline) - create_date).days



