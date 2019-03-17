from wtforms import *
from wtforms.validators import  *
from wtforms.fields.html5 import DateField, TelField
from flask_wtf import FlaskForm, Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    username = StringField('نوم',validators=[ length(min=6)])
    password = PasswordField('رمز',validators=[length(min=8,max=80)])
    remember=BooleanField('ياداښت')


class Register(FlaskForm):
    employee=SelectField("کاریګر", id='a',coerce=int,choices=[])
    username = StringField('نوم',validators=[ length(min=4)])
    password = PasswordField('رمز دا خل کړی', [
        validators.DataRequired(),
        validators.EqualTo('', message='ر مز باید یو شان وی')
    ])
    confirm = PasswordField('رمز بیا دا خل کړی')
    role = SelectField('رول', choices=[])
    active=BooleanField("فعالیت")


class UpdateUserForm(FlaskForm):

    role = SelectField('رول', choices=[])
    active=BooleanField("فعالیت")

class ResetPassword(FlaskForm):
    password = PasswordField('نوی رمز داخل کړی', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('رمز بیا دا خل کړی')


class StoreDrugForm(FlaskForm):
    dname = StringField('نوم', )
    type = SelectField('ډول', coerce=str,choices=[] )
    Category = SelectField('کټګوری', coerce=str,choices=[])
    company = SelectField('کمپنی', coerce=str,choices=[])
    barcode = StringField('بارکوډ',)

class DoctorReport(FlaskForm):
    profession = SelectField('مسلک انتخاب کړی', coerce=str,choices=[])

class SalaryReportForm(FlaskForm):
    emp = SelectField("کاریګر انتخاب کړی", coerce=str,choices=[])
    salaryDate = DateField('وخت انتخاب کړی', id = 'datetimepicker1')
    status = SelectField("اداینه",coerce=str,choices=[('paid', 'تادیه'), ('unpaid', 'ناتادیه')] )
    submit = SubmitField('پلټنه')

class TestFilterForm(FlaskForm):
    patient = SelectField("مریض انتخاب کړی", coerce=str,choices=[])
    doctor = SelectField("ډاکټر انتخاب کړی", coerce=str,choices=[])
    testType = SelectField("معاینات انتخاب کړی", coerce=int,choices=[])
    testDate = DateField('وخت انتخاب کړی')
    status = SelectField("حالت", coerce=str,choices=[('tested','معاینه شوی'), ('untested','نامعاینه شوی')])


class PayemntFilterForm(FlaskForm):

    patient = SelectField("مریض انتخاب کړی", coerce=str,choices=[])
    doctor = SelectField("ډاکټر انتخاب کړی", coerce=str,choices=[])
    date = DateField('وخت انتخاب کړی')
    status = SelectField("اداینه",coerce=str,choices=[('paid', 'تادیه'), ('unpaid', 'ناتادیه')] )

class TestPayemntFilterForm(FlaskForm):
    patient = SelectField("مریض انتخاب کړی", coerce=str,choices=[])
    test = SelectField("معاینات انتخاب کړی", coerce=str,choices=[])
    date = DateField('وخت انتخاب کړی')
    status = SelectField("اداینه",coerce=str,choices=[('paid', 'تادیه'), ('unpaid', 'ناتادیه')] )


class EmployeeForm(FlaskForm):
    name = StringField('نوم',  validators=[InputRequired()])
    phone = TelField('شمیره', validators=[InputRequired()])
    job = SelectField('وظیفه',coerce=str, choices=[], validators=[InputRequired()])
    address = StringField('ادرس', validators=[InputRequired()])
    nic_no = IntegerField('تذکیری شمیره')
    email = StringField('ایمیل')


class SalaryForm(FlaskForm):
    empNames=SelectField("کاریګر", id='a',coerce=str,choices=[])
    amount = FloatField('مقدار',  validators=[InputRequired('skjjk')])
    month = DateField('تاریخ', validators=[InputRequired()])
    status = SelectField("اداینه",coerce=str,choices=[('paid', 'تادیه'), ('unpaid', 'ناتادیه')] )


class DoctorForm(FlaskForm):

    empNames=SelectField("کاریګر",coerce=str,choices=[])
    profession=SelectField("مسلک", coerce=str,choices=[])
    room = IntegerField('وطاق',  validators=[InputRequired()])
    fee = FloatField('فیس', validators=[InputRequired()])

class AddPatientForm(FlaskForm):
   Id = HiddenField('')
   name = StringField(' د مریض نوم ' , validators=[InputRequired(), length(min=2, max=20, message=' نوم باید د ۱۰ څخه تر ۲ پوری وی ')])
   age = IntegerField('عمر')
   gender = SelectField('جنس', choices=[('Male', 'نارینه'),('Female', 'ښځینه')])
   phone = StringField('شمیره', validators=[length(max=10, message = 'شمیره باید لس عدده وی')])



class VisitFilterForm(FlaskForm):
   patient = SelectField("د مریض نوم دا خل کړی",coerce=str, choices=[])
   doctor = SelectField(' د ډاکټر نوم دا خل کړی ', coerce=str, choices=[] )
   action = SelectField(' کتنه ', coerce=str,choices=[('visited', 'لیدل شوی'), ('unvisited', 'نا لیدل شوی')])
   date = DateField('وخت انتخاب کړی', id = 'datetimepicker1')

  
class EmployeeReportForm(FlaskForm):
    job = SelectField("وظیفه",coerce=str, choices=[])


