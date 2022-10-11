from odoo import models, fields, api
from odoo import tools


class CustomReport(models.Model):
    _name = 'custom.report'
    _inherit = ['mail.thread']
    _auto = False
    _rec_name = 'company_name'
    _description = "TMX Custom CRM"

    partner_id = fields.Text(string="PartnerID", readonly=True)
    contact_id = fields.Text(string="ContactID", readonly=True)
    company_name = fields.Text(string="Company", readonly=True)
    contact_name = fields.Text(string="Contact", readonly=True)
    contact_email = fields.Text(string="Email", readonly=True)
    branch = fields.Char(string="Branch", readonly=True)
    year = fields.Text(string="Year", readonly=True)
    january = fields.Integer(string="January", readonly=True)
    february = fields.Integer(string="February", readonly=True)
    march = fields.Integer(string="March", readonly=True)
    april = fields.Integer(string="April", readonly=True)
    may = fields.Integer(string="May", readonly=True)
    june = fields.Integer(string="June", readonly=True)
    july = fields.Integer(string="July", readonly=True)
    august = fields.Integer(string="August", readonly=True)
    september = fields.Integer(string="September", readonly=True)
    october = fields.Integer(string="October", readonly=True)
    november = fields.Integer(string="November", readonly=True)
    december = fields.Integer(string="December", readonly=True)
    total = fields.Integer(string="Total", readonly=True)
    open_jobs = fields.Integer(string="Open Jobs", readonly=True)
    quotes = fields.Integer(string="Quotes", readonly=True)
    message_main_attachment_id = fields.Integer(string="message_main_attachment_id", readonly=False)
    phone_number = fields.Text(string='Phone Number', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""CREATE OR REPLACE VIEW %s AS (
                        select jb.id AS id, jb.partner_id, jb.contact_id, jb.company_name, jb.contact_name, 
                        jb.contact_email, jb.branch, 
                        jb.year, jb.january, jb.february, jb.march, jb.april, jb.may, jb.june, jb.july, jb.august, 
                        jb.september, jb.october, jb.november, 
                        jb.december,(january+february+march+april+may+june+july+august+september+october+november+december) 
                        as total, jb.open_jobs, jb.quotes, jb.message_main_attachment_id, 
                        fn_get_phones_and_mobiles_by_contact(jb.contact_id) as phone_number
                        FROM jobs_contacts_year_branch jb
                  		order by jb.company_name)""" % (self._table,))

    def _query(self):
        query = """SELECT distinct partner_id
                           FROM custom_report
                          WHERE id = %s """
        self._cr.execute(query, [self.id])
        rec = self.browse(row[0] for row in self._cr.fetchall())
        return rec

    def action_get_invoices(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        pid = self._query()
        action['domain'] = [
            ('partner_id', 'child_of', int(pid)),
            ('move_type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')),
        ]
        action['context'] = {'default_move_type': 'out_invoice', 'move_type': 'out_invoice', 'journal_type': 'sale'}
        return action

    def _query_contact(self):
        query = """SELECT distinct contact_id
                           FROM custom_report
                          WHERE id = %s limit 1"""
        self._cr.execute(query, [self.id])
        return [row[0] for row in self._cr.fetchall()]

    def _query_email(self):
        query = """SELECT distinct contact_email
                           FROM custom_report
                          WHERE id = %s """
        self._cr.execute(query, [self.id])
        return [row[0] for row in self._cr.fetchall()]
        # rec = self.browse(row[0] for row in self._cr.fetchall())
        # return rec

    def open_custom_view(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale.action_custom_hist')
        em = self._query_email()
        action['domain'] = [('originator_email', '=', em), ('docu_type', '=', 'JOB')]
        return action

    def open_custom_quote(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale.action_custom_hist')
        em = self._query_email()
        action['domain'] = [('originator_email', '=', em), ('docu_type', '=', 'QUOTE')]
        return action

    def open_crm_profile(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale.action_crm_profile')
        cid = self._query_contact()
        action['domain'] = [('contact_id', '=', cid)]
        return action