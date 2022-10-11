from odoo import models, fields, api
from odoo import tools


class CustomTrack(models.Model):
    _name = 'custom.tracking'
    _auto = False
    _rec_name = 'company_name'
    _description = "TMX Tracking"

    reference = fields.Text(string="Ref.", readonly=True)
    docu_type = fields.Text(string="Type", readonly=True)
    creation_date = fields.Datetime(string="Log Date", readonly=True)
    originator_email = fields.Text(string="Email", readonly=True)
    company_name = fields.Text(string="Name", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""CREATE OR REPLACE VIEW %s AS (
                        select id as id, reference, docu_type, creation_date, originator_email, company_name, 
                        message_main_attachment_id
                        from jobs_quotes_tracking where docu_type = 'TRACKING'
                  		order by creation_date desc)""" % (self._table,))

    def _query_email(self):
        query = """SELECT distinct originator_email
                           FROM custom_tracking
                          WHERE id = %s"""
        self._cr.execute(query, [self.id])
        return [row[0] for row in self._cr.fetchall()]

    def open_detail_view(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale.action_custom_profile')
        em = self._query_email()
        action['domain'] = [('originator_email', '=', em)]
        return action