from src.connection import app, db

from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager

from flask_migrate import Migrate

# import flask_whooshalchemyplus as wa
from datetime import datetime, date
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, roles_required


Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)

class DrugType(db.Model):

    __tablename__='cms_tbl_drugTypes'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)
    drugs=db.relationship('Drug', backref='cms_tbl_drugTypes', lazy='dynamic')

    def store(self, name):
        self.name=name

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def __repr__(self):
        return '{0} {1}'.format(self.id, self.name)

    def show(self):
        return self.query.all()

class Company(db.Model):

    __tablename__='cms_tbl_companies'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)
    drugs=db.relationship('Drug', backref='cms_tbl_companies', lazy='dynamic')

    def store(self, name):
        self.name=name

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def __repr__(self):
        return '{0} {1}'.format(self.id, self.name)

    def show(self):
        return self.query.all()

class Category(db.Model):

    __tablename__='cms_tbl_categories'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)
    drugs=db.relationship('Drug', backref='cms_tbl_categories', lazy='dynamic')


    def store(self, name):
        self.name=name

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def __repr__(self):
        return '{0} {1}'.format(self.id, self.name)

    def show(self):
        return self.query.all()


class Drug(db.Model):
    __tablename__='cms_tbl_drugs'
    #__searchable__=['drugName']

    drugId=db.Column(db.Integer, primary_key=True)
    drugName=db.Column(db.Text)
    drugType=db.Column(db.Integer, db.ForeignKey('cms_tbl_drugTypes.id'))
    companyName=db.Column(db.Integer, db.ForeignKey('cms_tbl_companies.id', ondelete='RESTRICT'))
    categoryName = db.Column(db.Integer, db.ForeignKey('cms_tbl_categories.id'))
    barcode=db.Column(db.Text)
    purchases=db.relationship('Purchase', backref='cms_tbl_drugs', lazy='dynamic')
    sales=db.relationship('Sale', backref='cms_tbl_drugs', lazy='dynamic')
    createdDate = db.Column(db.DateTime, index=True, default=datetime.now())


    def __init__(self):
        pass#wa.whoosh_index(app, Drug)

    def store(self, drugName, drugType, companyName, categoryName, barcode):

        self.drugName=drugName
        self.drugType=drugType
        self.companyName=companyName
        self.categoryName=categoryName
        self.barcode=barcode

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def __repr__(self):
        return '{0} {1} {2} {3} {4} {5}'.format(self.drugId,self.drugName, self.drugType, self.companyName, self.categoryName, self.barcode)

    def show(self):
        return self.query.all()

    def update(self, drugId, drugName, drugType, companyName, categoryName, barcode):

        self.drugId=drugId
        self.drugName=drugName
        self.drugType=drugType
        self.companyName=companyName
        self.categoryName=categoryName
        self.barcode=barcode

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, drugId):
        record=self.query.get(drugId)

        db.session.delete(record)
        db.session.commit()

    def getBybcr(self, barcode):
        return self.query.filter(Drug.barcode==barcode).all()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()

class Purchase(db.Model):
    __tablename__='cms_tbl_purchases'
   # __searchable=['name']

    purchaseId=db.Column(db.Integer, primary_key=True)
    drugId=db.Column(db.Integer, db.ForeignKey("cms_tbl_drugs.drugId"))
    drugPrice=db.Column(db.Float)
    drugQuantity=db.Column(db.Float)
    purchaseDate=db.Column(db.Date)
    drugExpirDate=db.Column(db.Date)


    def __init__(self):
        pass#wa.whoosh_index(app, Purchase)

    def __repr__(self):
        return '{0} {1} {2} {3} {4} {5}'.format(self.purchaseId, self.drugId, self.drugPrice, self.drugQuantity, self.purchaseDate, self.drugExpirDate)

    def store(self, drugId, drugPrice, drugQuantity, purchaseDate, drugExpirDate):

        self.drugId = drugId
        self.drugPrice = drugPrice
        self.drugQuantity = drugQuantity
        self.purchaseDate = purchaseDate
        self.drugExpirDate = drugExpirDate

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, purchaseId, drugId, drugPrice, drugQuantity, purchaseDate, drugExpirDate):

        self.purchaseId=purchaseId
        self.drugId=drugId
        self.drugPrice=drugPrice
        self.drugQuantity=drugQuantity
        self.purchaseDate=purchaseDate
        self.drugExpirDate=drugExpirDate

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, purchaseId):
        record = self.query.get(purchaseId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class Sale(db.Model):
    __tablename__ = 'cms_tbl_sales'
   # __searchable=['name']

    saleId = db.Column(db.Integer, primary_key=True)
    drugId = db.Column(db.Integer, db.ForeignKey("cms_tbl_drugs.drugId"))
    drugPrice = db.Column(db.Float)
    drugQuantity = db.Column(db.Float)
    billNo=db.Column(db.Integer)
    userId=db.Column(db.Integer, db.ForeignKey("users.id"))
    saleDate = db.Column(db.DateTime, index=True, default=datetime.now())

    def __init__(self):
        pass#wa.whoosh_index(app, sale)

    def __repr__(self):
        return '{0} {1} {2} {3} {4} {5} {6}'.format(self.saleId, self.drugId, self.drugPrice, self.drugQuantity, self.saleDate, self.billNo, self.userId)

    def store(self, drugId, drugPrice, drugQuantity, billNo, userId):

        self.drugId=drugId
        self.drugPrice=drugPrice
        self.drugQuantity=drugQuantity
        self.billNo=billNo
        self.userId=userId

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, saleId, drugId, drugPrice, drugQuantity, billNo, userId):

        self.saleId=saleId
        self.drugId=drugId
        self.drugPrice=drugPrice
        self.drugQuantity=drugQuantity
        self.billNo=billNo
        self.userId = userId

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, saleId):
        record = self.query.get(saleId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class Return(db.Model):
    __tablename__ = 'cms_tbl_returns'
   # __searchable=['name']

    returnId = db.Column(db.Integer, primary_key=True)
    saleId = db.Column(db.Integer, db.ForeignKey("cms_tbl_sales.saleId"))
    purchasePrice = db.Column(db.Float)
    drugQuantity = db.Column(db.Float)
    returnDate = db.Column(db.Date)

    def __init__(self):
        #wa.whoosh_index(app, Return)
        pass

    def __repr__(self):
        return '{0} {1} {2} {3} {4}'.format(self.returnId, self.saleId, self.purchasePrice, self.drugQuantity, self.returnDate)

    def store(self, saleId, purchasePrice, drugQuantity, returnDate):

        self.saleId=saleId
        self.purchasePrice=purchasePrice
        self.drugQuantity=drugQuantity
        self.returnDate=returnDate

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, returnId, saleId, purchasePrice, drugQuantity, returnDate):

        self.returnId=returnId
        self.saleId=saleId
        self.purchasePrice=purchasePrice
        self.drugQuantity=drugQuantity
        self.returnDate=returnDate

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, returnId):
        record = self.query.get(returnId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    employeeId=db.Column(db.Integer, db.ForeignKey('cms_tbl_employees.employeeId'))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    roles = db.relationship('Role', secondary='user_roles')


    def delete(self, id):
        record = self.query.get(id)

        db.session.delete(record)
        db.session.commit()


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


class Job(db.Model):

    __tablename__='cms_tbl_jobs'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.LargeBinary)
    employees=db.relationship('Employee', backref='cms_tbl_jobs', lazy='dynamic')

    def store(self, name):
        self.name=name.encode('utf-8')

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def __repr__(self):
        return '{0} {1}'.format(self.id, self.name)

    def show(self):
        return self.query.all()

class Profession(db.Model):

    __tablename__='cms_tbl_professions'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.LargeBinary)
    doctors=db.relationship('Doctor', backref='cms_tbl_professions', lazy='dynamic')

    def store(self, name):
        self.name=name.encode('utf-8')

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def __repr__(self):
        return '{0} {1}'.format(self.id, self.name)

    def show(self):
        return self.query.all()


class Doctor(db.Model):
    __tablename__ = 'cms_tbl_doctors'
   # __searchable=['name']

    doctorId = db.Column(db.Integer, primary_key=True)
    employeeId=db.Column(db.Integer, db.ForeignKey('cms_tbl_employees.employeeId'))
    profession = db.Column(db.Integer, db.ForeignKey('cms_tbl_professions.id'))
    roomNumber = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    visits = db.relationship('Visit', backref='cms_tbl_doctors', lazy='dynamic')

    def __init__(self):
        pass#wa.whoosh_index(app, Doctor)

    def __repr__(self):
        return '{0} {1} {2} {3} {4}'.format(self.doctorId, self.employeeId, self.profession, self.roomNumber, self.fee)

    def store(self, employeeId, profession, roomNumber, fee):

        self.employeeId=employeeId
        self.profession=profession
        self.roomNumber=roomNumber
        self.fee = fee

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, doctorId, employeeId, profession, roomNumber, fee):

        self.doctorId=doctorId
        self.employeeId = employeeId
        self.profession = profession
        self.roomNumber = roomNumber
        self.fee = fee

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, doctorId):
        record = self.query.get(doctorId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class Patient(db.Model):
    __tablename__ = 'cms_tbl_patients'
   # __searchable=['name']

    patientId = db.Column(db.Integer, primary_key=True)
    patientName = db.Column(db.LargeBinary)
    patientAge = db.Column(db.Integer)
    gender = db.Column(db.Text)
    phoneNumber = db.Column(db.String(10), unique = True)
    visitDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    visits = db.relationship('Visit', backref='cms_tbl_patients', lazy='dynamic')
    # payments =


    def __init__(self):
        pass#wa.whoosh_index(app, Patient)

    def __repr__(self):
        return '{0} {1} {2} {3} {4}'.format(self.patientId, self.patientName.decode('utf-8'), self.patientAge, self.gender, self.phoneNumber)

    def store(self, patientName, patientAge, gender, phoneNumber ):

        self.patientName=patientName
        self.patientAge=patientAge
        self.gender=gender
        self.phoneNumber=phoneNumber

        # self.visitDate=visitDate
        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, patientId, patientName, patientAge, gender, phoneNumber):

        self.patientId=patientId
        self.patientName = patientName
        self.patientAge = patientAge
        self.gender = gender
        self.phoneNumber = phoneNumber

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, patientId):
        record = self.query.get(patientId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()

class Employee(db.Model):
    __tablename__ = 'cms_tbl_employees'
   # __searchable=['name']
    employeeId = db.Column(db.Integer, primary_key=True)
    employeeName = db.Column(db.LargeBinary)
    phoneNumber = db.Column(db.Text)
    homeAddress = db.Column(db.LargeBinary)
    NIC_No = db.Column(db.Integer)
    employeeJob = db.Column(db.Integer, db.ForeignKey('cms_tbl_jobs.id'))
    employeeEmail = db.Column(db.Text)
    employeePhoto = db.Column(db.Text)
    users=db.relationship('User', backref='cms_tbl_employees', lazy='dynamic')
    sallaries=db.relationship('Salary', backref='cms_tbl_employees', lazy='dynamic')
    doctors=db.relationship('Doctor', backref='cms_tbl_employees', lazy='dynamic')

    def __init__(self):
        pass#wa.whoosh_index(app, Employee)

    def __repr__(self):
        return '{0} {1} {2} {3} {4} {5} {6} {7}'.format(self.employeeId, self.employeeName.decode('utf-8'), self.phoneNumber, self.homeAddress.decode('utf-8'), self.NIC_No, self.employeeJob, self.employeeEmail, self.employeePhoto)
        # return '{0}'.format(self.employeeName.decode('utf-8'))
        pass

    def store(self, employeeName, phoneNumber, homeAddress, NIC_No, employeeJob, employeeEmail):

        self.employeeName=employeeName
        self.phoneNumber=phoneNumber
        self.homeAddress=homeAddress
        self.NIC_No=NIC_No
        self.employeeJob=employeeJob
        self.employeeEmail=employeeEmail

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def showEmployeeNames(self):

        return Employee.query.with_entities(Employee.employeeName.decode('utf-8'))

    def showEmployeeByID(self, empName):

        return Employee.query.with_entities(Employee.employeeId).filter(Employee.employeeName == empName)

    def update(self, employeeId, employeeName, phoneNumber, homeAddress, NIC_No, employeeJob, employeeEmail):

        self.employeeId=employeeId
        self.employeeName = employeeName
        self.phoneNumber = phoneNumber
        self.homeAddress = homeAddress
        self.NIC_No = NIC_No
        self.employeeJob = employeeJob
        self.employeeEmail = employeeEmail

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, employeeId):
        record = self.query.get(employeeId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class Salary(db.Model):
    __tablename__ = 'cms_tbl_salaries'
   # __searchable=['name']

    salaryId = db.Column(db.Integer, primary_key=True)
    employeeID = db.Column(db.Integer, db.ForeignKey('cms_tbl_employees.employeeId'))
    month = db.Column(db.Date)
    amount = db.Column(db.Float)
    status = db.Column(db.Text)

    def __init__(self):
        pass#wa.whoosh_index(app, Salary)

    def __repr__(self):
        return '{0} {1} {2} {3} {4}'.format(self.sallaryId, self.employeeID, self.month, self.amount, self.status)

    def store(self, employeeID, month, amount, status):

        self.employeeID=employeeID
        self.month=month
        self.amount=amount
        self.status=status

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, salaryId, employeeID, month, amount, status):

        self.salaryId=salaryId
        self.employeeID = employeeID
        self.month = month
        self.amount = amount
        self.status = status

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, salaryId):
        record = self.query.get(salaryId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class TestType(db.Model):
    __tablename__ = 'cms_tbl_testTypes'
   # __searchable=['name']

    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30), unique = True)
    Amount = db.Column(db.Float)
    tests = db.relationship('Test', backref='cms_tbl_testTypes', lazy='dynamic')
    createdDate = db.Column(db.DateTime, index=True, default=datetime.now())

    def __init__(self):
        pass#wa.whoosh_index(app, Patient)

    def __repr__(self):
        return '{0} {1} {2}'.format(self.Id, self.Name, self.Amount)

    def store(self, Name, Amount):

        self.Name=Name
        self.Amount=Amount

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, Id, Name, Amount):

        self.Id=Id
        self.Name = Name
        self.Amount = Amount

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, Id):
        record = self.query.get(Id)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class Test(db.Model):
    __tablename__ = 'cms_tbl_tests'
   # __searchable=['name']

    testId = db.Column(db.Integer, primary_key=True)
    typeId = db.Column(db.Integer, db.ForeignKey('cms_tbl_testTypes.Id'))
    testDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    action=db.Column(db.Text)
    tests = db.relationship('Payment',cascade = "all, delete-orphan" , backref='cms_tbl_patients', lazy='dynamic')
    createdDate = db.Column(db.DateTime, index=True, default=datetime.now())

    attachment = db.Column(db.Text)

    def __init__(self):
        pass#wa.whoosh_index(app, Test)

    def __repr__(self):
        return '{0} {1} {2} {3} {4}'.format(self.testId, self.typeId, self.testDate, self.action, self.attachment)

    def store(self, typeId):

        self.typeId=typeId
        self.action='untested'

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()


    def update(self, testId,typeId):

        self.testId=testId

        self.typeId = typeId
        self.action='tested'
        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, testId):
        record = self.query.get(testId)

        db.session.delete(record)
        db.session.commit()

    def wsr(self, input_text):
        return self.query.whoosh_search(input_text, like=True, or_=True, limit=40).all()


class Visit(db.Model):
    __tablename__='cms_tbl_visits'

    visitId=db.Column(db.Integer, primary_key=True)
    patientId=db.Column(db.Integer, db.ForeignKey('cms_tbl_patients.patientId'))
    doctorId=db.Column(db.Integer, db.ForeignKey('cms_tbl_doctors.doctorId'))
    action=db.Column(db.Text)
    payments = db.relationship('Payment', cascade= "all, delete-orphan", backref='cms_tbl_visits', lazy='dynamic')
    visitDate = db.Column(db.DateTime, index=True, default=datetime.now())


    def __init__(self):
        pass

    def __repr__(self):
        return '{0} {1} {2} {3} {4}'.format()

    def store(self, patientId, doctorId):

        self.patientId=patientId
        self.doctorId=doctorId
        self.action = "unvisited"

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, visitId, doctorId):

        self.visitId=visitId
        self.doctorId = doctorId


        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def delete(self, visitId):
        record=self.query.get(visitId)

        db.session.delete(record)
        db.session.commit()

class Payment(db.Model):
    __tablename__='cms_tbl_payments'

    Id=db.Column(db.Integer, primary_key=True)
    visitId=db.Column(db.Integer, db.ForeignKey('cms_tbl_visits.visitId'))
    testId=db.Column(db.Integer, db.ForeignKey('cms_tbl_tests.testId'), nullable = True)
    amount = db.Column(db.Float)
    amountStatus = db.Column(db.Text)
    discount = db.Column(db.Float)
    date = db.Column(db.Date, index=True, default=datetime.utcnow)


    def __init__(self):
        pass

    def __repr__(self):
        return '{0} {1} {2} {3} {4} {5}'.format(self.Id, self.testId, self.amount, self.amountStatus, self.discount, self.date)

    def storeDoctorPayment(self, visitId):

        self.visitId=visitId
        self.amountStatus = 'paid'

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def storeLabPayment(self, visitId, f):
        self.visitId=visitId
        self.testId = f
        self.amountStatus = "unpaid"

        with app.app_context():
            db.session.merge(self)
            db.session.commit()

    def show(self):
        return self.query.all()

    def update(self, paymentId, testId):
        record=self.query.get(paymentId)

        record.testId=testId
        record.amountStatus="paid"

        with app.app_context():
            db.session.merge(record)
            db.session.commit()

    def delete(self, Id):
        record=self.query.get(Id)

        db.session.delete(record)
        db.session.commit()
