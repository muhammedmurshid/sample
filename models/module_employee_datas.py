from odoo import fields, models, _
import io
import cairosvg


class EmployeeModuleForm(models.Model):
    _name = 'employee.module.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_name'
    _description = "Joining Form"

    bank_name = fields.Char(string='Bank Name')
    spouse_name = fields.Char(string='Spouse Name')
    name_of_children = fields.Text(string='Name Of Childrens')
    bank_acc_number = fields.Char(string='Account Number')
    branch_bank = fields.Char(string='Branch')
    ifsc_code = fields.Char(string='IFSC Code')
    micr_code = fields.Char(string='MICR Code')
    name_as_per_bank = fields.Char(string='Name As Per Bank Account')
    aadhar_card_number = fields.Integer(string='Aadhar Card Number')
    name_as_per_aadhar = fields.Char(string='Name As Per Aadhaar Card')
    pan_card_number = fields.Char(string='Pan Card Number')
    name_as_per_pan = fields.Char(string='Name As Per Pan Card')
    pf_uan_number = fields.Char(string='PF UAN Number')
    esi_ip_number = fields.Char(string='ESI IP Number')
    blood_group = fields.Char(string='Blood Group')
    employee_name = fields.Char(string='Employee Name')
    designation = fields.Char(string='Designation')
    date_of_joining = fields.Date(string='Date Of Joining')
    date_of_birth = fields.Date(string='Date Of Birth')
    mail_id = fields.Char(string='Email')
    phone_number = fields.Char(string='Personal Phone Number')
    office_phone = fields.Char(string='Office Phone Number')
    office_mail = fields.Char(string='Office Email')
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    mother_dob = fields.Date(string='Mother Date Of Birth')
    father_dob = fields.Date(string='Father Date Of Birth')
    spouse_dob = fields.Date(string='Spouse Date Of Birth')
    marital_stats = fields.Char(string='Marital Status')
    address = fields.Text(string='Address')
    fath_rel = fields.Char(string='Father Relation')
    moth_rel = fields.Char(string='Mother Relation')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')
    upload_cv = fields.Binary(string='Upload CV')

    def confirm_employee_request(self):
        print("hr_approval")

        self.state = 'confirm'

    def cancel_employee_request(self):
        self.state = 'cancel'

    def confirm_technical_officer(self):
        abc = []
        for rec in self:
            res_list = {
                'member_name': rec.father_name,
                # 'relation_id': 'father',
                # 'classroom_id': self.class_room.name,
                'birth_date': rec.father_dob,


            }
            res_list_mom = {
                'member_name': rec.mother_name,
                # 'relation_id': 'mother',
                # 'classroom_id': self.class_room.name,
                'birth_date': rec.mother_dob,

            }
            abc.append((0, 0, res_list))
            abc.append((0, 0, res_list_mom))

        if self.marital_stats == 'married':
            self.env['hr.employee'].create({
                'marital': 'married',
                'name': self.employee_name,
                'job_title': self.designation,
                'work_email': self.mail_id,
                'mobile_phone': self.phone_number,
                'home_address': self.address,
                'birthday': self.date_of_birth,
                'joining_date_cus': self.date_of_joining,
                'bank_name': self.bank_name,
                'bank_acc_number': self.bank_acc_number,
                'branch_bank': self.branch_bank,
                'ifsc_code': self.ifsc_code,
                'micr_code': self.micr_code,
                'name_as_per_bank': self.name_as_per_bank,
                'aadhar_card_number': self.aadhar_card_number,
                'name_as_per_aadhar': self.name_as_per_aadhar,
                'pan_card_number': self.pan_card_number,
                'name_as_per_pan': self.name_as_per_pan,
                'pf_uan_number': self.pf_uan_number,
                'esi_ip_number': self.esi_ip_number,
                'blood_group': self.blood_group,
                'spouse_birthdate': self.spouse_dob,
                'spouse_complete_name': self.spouse_name,
                'children_name': self.name_of_children,
                'fam_ids': abc


            }
            )
        else:
            self.env['hr.employee'].create({
                'name': self.employee_name,
                'job_title': self.designation,
                'work_email': self.mail_id,
                'mobile_phone': self.phone_number,
                'home_address': self.address,
                'birthday': self.date_of_birth,
                'joining_date': self.date_of_joining,
                'bank_name': self.bank_name,
                'bank_acc_number': self.bank_acc_number,
                'branch_bank': self.branch_bank,
                'ifsc_code': self.ifsc_code,
                'micr_code': self.micr_code,
                'name_as_per_bank': self.name_as_per_bank,
                'aadhar_card_number': self.aadhar_card_number,
                'name_as_per_aadhar': self.name_as_per_aadhar,
                'pan_card_number': self.pan_card_number,
                'name_as_per_pan': self.name_as_per_pan,
                'pf_uan_number': self.pf_uan_number,
                'esi_ip_number': self.esi_ip_number,
                'blood_group': self.blood_group,
                'fam_ids': abc,
                'spouse_complete_name': self.spouse_name,
                'children_name': self.name_of_children,

            }
            )
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('logic_employee_form.mail_activity_joining_form').id)])
        activity_id.action_feedback(feedback=f'Confirmed {self.env.user.name}')
        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('logic_employee_form.mail_activity_joining_form').id)])
        other_activity_ids.unlink()
        self.state = 'done'

    def return_employee_request(self):
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('logic_employee_form.mail_activity_joining_form').id)])
        activity_id.action_feedback(feedback=f'Returned {self.env.user.name}')
        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('logic_employee_form.mail_activity_joining_form').id)])
        other_activity_ids.unlink()
        self.state = 'draft'

    def technical_activity(self):
        print('hhhi')
        ss = self.env['employee.module.form'].search([])
        for i in ss:
            if i.state == 'confirm':
                users = ss.env.ref('logic_employee_form.joining_form_for_technical_officer').users
                for j in users:
                    activity_type = i.env.ref('logic_employee_form.mail_activity_joining_form')
                    i.activity_schedule('logic_employee_form.mail_activity_joining_form', user_id=j.id,
                                        note=f'Please Confirm Joining Form {j.name}')

    name_ids = fields.One2many('one.many', 'name_id', string='Name')


class OneMany(models.Model):
    _name = 'one.many'

    name = fields.Char(string='Name')
    name_id = fields.Many2one('employee.module.form', string='Name')
