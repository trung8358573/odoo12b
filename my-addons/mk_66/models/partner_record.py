# -*- coding: utf-8 -*-
from odoo import fields, models, api


class City(models.Model):
    _name = "res.city"
    _description = 'City'

    country_id = fields.Many2one('res.country', string='Country', required=True)
    name = fields.Char('Name', required=True)


class School(models.Model):
    _name = "res.school"
    _inherit = 'res.partner'
    _description = 'School'

    type = fields.Selection([
        ('school', 'School'),
        ('uni', 'University'), ], string='Type', default='school')
    college_partner_ids = fields.One2many('res.partner.record', 'college_id', string='Attended')
    hs_partner_ids = fields.One2many('res.partner.record', 'high_school_id', string='Attended')


class Activity(models.Model):
    _name = "res.activity"
    _description = 'Activity'

    name = fields.Char('Name')
    college_partner_ids = fields.Many2many('res.partner.record', 'partner_record_college_activity_rel', 'aid', 'pid',
                                           string='College Partners')
    current_partner_ids = fields.Many2many('res.partner.record', 'partner_record_current_activity_rel', 'aid', 'pid',
                                           string='Current Partners')


class Partner(models.Model):
    _inherit = 'res.partner'

    city_id = fields.Many2one('res.city', string='City')


class PartnerRecord(models.Model):
    _name = "res.partner.record"
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Partner Record'

    partner_id = fields.Many2one('res.partner', domain=[('is_company', '=', False)], string='Customer', required=True)
    nick_name = fields.Char('Nick Name')
    dob = fields.Date('Date of Birth')
    birth_place = fields.Char('Birth Place')
    home_town = fields.Many2one('res.city', string='Home Town')
    height = fields.Float('Height (cm)')
    weight = fields.Float('Weight (kg)')

    high_school_id = fields.Many2one('res.school', string='High School', domain=[('type', '=', 'school')])
    college_id = fields.Many2one('res.school', string='University', domain=[('type', '=', 'uni')])
    high_school_date = fields.Date('Date of High School Graduation')
    college_date = fields.Date('Date of College Graduation')
    college_activity_ids = fields.Many2many('res.activity', 'partner_record_college_activity_rel', 'pid', 'aid',
                                            string='College Extracurricular Activity')
    current_activity_ids = fields.Many2many('res.activity', 'partner_record_current_activity_rel', 'pid', 'aid',
                                            string='Current Extracurricular Activity')
    college_activity_groups = fields.Many2many('res.partner', domain=[('is_company', '=', True)],
                                               string='College Activity Groups')
    military_service = fields.Text(string="Military Service")
    military_rank = fields.Char(string="Military Discharge Rank")
    military_attitude = fields.Text(string="Attitude Toward Being In The Military")

    spouse_id = fields.Many2one('res.partner.record', string='Spouse')
    spouse_college_id = fields.Many2one('res.school', string='Spouse Education', related='spouse_id.college_id')
    spouse_activity_ids = fields.Many2many('res.activity', related='spouse_id.current_activity_ids')
