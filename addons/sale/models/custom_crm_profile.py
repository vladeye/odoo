from odoo import models, fields, api
from odoo import tools


class CustomCrmProf(models.Model):
    _name = 'crm.profile'
    _inherit = ['mail.thread']
    _auto = False
    _rec_name = 'company_name'
    _description = "CRM Profile"

    contact_id = fields.Integer(string="Contact ID", readonly=True)
    partner_id = fields.Integer(string="Partner ID", readonly=True)
    company_name = fields.Text(string="Company", readonly=True)
    contact_name = fields.Text(string="Name", readonly=True)
    contact_email = fields.Text(string="Email", readonly=True)
    phone_number = fields.Text(string="Phone Number", readonly=True)
    message_main_attachment_id = fields.Integer(string="message_main_attachment_id", readonly=False)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""CREATE OR REPLACE VIEW %s AS (
                        select distinct contact_id as id, contact_id, partner_id, company_name, contact_name, contact_email, 
                        fn_get_phones_and_mobiles_by_contact(contact_id) as phone_number, message_main_attachment_id 
                        from jobs_contacts_year_branch)""" % (self._table,))

    # def _query_email(self):
    #     query = """SELECT distinct originator_email
    #                        FROM custom_profile
    #                       WHERE id = %s """
    #     self._cr.execute(query, [self.id])
    #     return [row[0] for row in self._cr.fetchall()]
    #
    # def open_detail_view(self):
    #     action = self.env['ir.actions.act_window']._for_xml_id('sale.action_custom_profile')
    #     em = self._query_email()
    #     action['domain'] = [('originator_email', '=', em)]
    #     return action