from odoo import models, fields

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
    property_type_id = fields.Many2one("estate.property.type", string="Type")  # Corrected model name
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
    garden_orientation = fields.Selection(string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Select type")


class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = "Estate Property Type model"

    name = fields.Char(required=True)