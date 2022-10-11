from odoo import models, fields, api
from odoo import tools


class CustomHist(models.Model):
    _name = 'custom.hist'
    _auto = False
    _rec_name = 'originator_email'
    _description = "TMX Historic"

    originator_email = fields.Text(string="Email", readonly=True)
    docu_type = fields.Text(string="Type", readonly=True)
    creation_date = fields.Date(string="Creation Date", readonly=True)
    company_name = fields.Text(string="Company", readonly=True)
    ship_to_name = fields.Text(string="Ship to Name", readonly=True)
    ship_to_city = fields.Text(string="Ship to City", readonly=True)
    ship_to_state = fields.Text(string="Ship to State", readonly=True)
    ship_to_zipcode = fields.Text(string='Zipcode', readonly=True)
    branch = fields.Char(string="Branch", readonly=True)
    reference = fields.Text(string="Ref.", readonly=True)
    job_type = fields.Text(string="Job Type", readonly=True)
    total_jobs = fields.Integer(string="Total JOBS", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""CREATE OR REPLACE VIEW %s AS (
                        select  id as id, originator_email, docu_type, creation_date, company_name, ship_to_name, ship_to_city, 
                        ship_to_state, ship_to_zipcode, branch, reference, job_type,
                        case WHEN docu_type = 'JOB' THEN 1 ELSE 0 END total_jobs
                        from jobs_quotes_tracking where docu_type != 'TRACKING'
                  		order by company_name)""" % (self._table,))
