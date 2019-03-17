from flask import render_template, request,jsonify, redirect, flash, url_for, Response
import json
from src.dataModel import *
from flask_wtf import FlaskForm, Form
from wtforms import *
from flask_bootstrap import Bootstrap
from wtforms.validators import *
from wtforms.widgets import *
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from src.forms import *
from sqlalchemy import inspect, text
from flask_user import current_user
from subprocess import call
import random, barcode
value=0

# sales routes

class Decoding:
    def doctorNames(self):
        doctors = db.session.query(Doctor.doctorId, Employee.employeeName).filter(Doctor.employeeId == Employee.employeeId).all()
        data=dict()
        data[''] = ''

        for doctor in doctors:
            data[doctor.doctorId]=doctor.employeeName.decode('utf-8')

        return (list(data.items()))

    def patientNames(self):
        patients = db.session.query(Patient.patientId, Patient.patientName).all()
        data=dict()
        data[''] = ''

        for patient in patients:
            data[patient.patientId]=patient.patientName.decode('utf-8')
        return (list(data.items()))

    def testNames(self):
        testTypes = db.session.query(TestType.Id, TestType.Name).all()
        return (testTypes)

    def employeeNames(self):
        employees = db.session.query(Employee.employeeId, Employee.employeeName).all()
        data=dict()
        data[''] = ''


        for employee in employees:
            data[employee.employeeId]=employee.employeeName.decode('utf-8')

        return (list(data.items()))

    def professionNames(self):
        professions = db.session.query(Profession.id, Profession.name).all()
        data=dict(professions)
        data[''] = ''


        for profession in professions:
            data[profession.id]=profession.name.decode('utf-8')

        return(list(data.items()))


    def jobNames(self):
        jobs = db.session.query(Job.id, Job.name).all()
        data=dict(jobs)
        data[''] = ''


        for job in jobs:
            data[job.id]=job.name.decode('utf-8')

        return(list(data.items()))

    def compnayNames(self):
        companies =  db.session.query(Company.id, Company.name).all()

        return(companies)

    def drugTypeNames(self):
        types =  db.session.query(DrugType.id, DrugType.name).all()


        return(types)

    def drugCategoryNames(self):
        categories =  db.session.query(Category.id, Category.name).all()


        return(categories)



'''class PayemntFilterForm(FlaskForm):
    decoding = Decoding()
    patient = QuerySelectField("مریض انتخاب کړی",query_factory=Decoding.patientNames(), get_label= "نسیت", allow_blank=True)
    doctor = SelectField("ډاکټر انتخاب کړی", coerce=int,choices=[])
    date = DateField('وخت انتخاب کړی')
    status = SelectField("اداینه",coerce=str,choices=[('', 'تادیه'), ('', 'ناتادیه')] )'''




#@app.route('/admin/bill', methods = ['GET'])
@app.route('/admin/sale')
def sale():
   return render_template("admin/bill.html")



@app.route('/saleReport')
def saleReport():

    datals=db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId==Drug.drugId)).join(User, (User.id==Sale.userId)).join(Employee, (Employee.employeeId==User.employeeId)).all()
    return render_template("admin/saleReport.html", data=datals)

@app.route('/store', methods=['POST'])
def store():
    try:
        sale=Sale()

        data=request.get_json()
        result=""

        if data:
            for d in data:
                sell.store(drugId=d['productId'], drugQuantity=d['qty'], drugPrice=d['price'], billNo=d['billNo'], userId=d['sellerId'])
                result+=d['product']+" | "+d['productId']+" | "+d['qty']+" | "+d['price']+" | "+d['billNo']+" | "+d['sellerId']+"\n"
            print(result)

        return "done"
    except Exception as e:
        print(str(e))

    return "wow"

@app.route('/tackBCR')
def tackBCR():
    try:
        drug=Drug()
        data=request.args.get('brcode')
        print(type(data))
        pur=Purchase()
        s=Sale()

        drugls=drug.getBybcr(data)
        price=pur.query.filter(Purchase.drugId==drugls[0].drugId).all()
        print(drugls)
        if not price[0].drugPrice:
            price[0].drugPrice=0
            print(price[0].drugPrice)

        billNo = db.session.query(Sale.billNo).order_by(Sale.saleId.desc()).first()
        #billNo=s.query.all()[-1].billNo+1
        if not billNo:
            billNo=1
        else:
            billNo=int(billNo[0])+1

        print(drugls[0].drugType, billNo)
        return jsonify(result=(drugls[0].drugName, drugls[0].drugId, price[0].drugPrice, billNo))

    except Exception as e:
        print(str(e))
        return 'not found'

@app.route('/saleBydate')
def saleByDate():
    drugId=request.args.get('drugId')
    fromDate=request.args.get('from')
    toDate=request.args.get('to')
    saler=request.args.get('saler')
    datals=[]

    if fromDate and toDate and drugId and saler:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(User, (User.id == Sale.userId)).join(
            Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate >= datetime.strptime(fromDate, '%Y-%m-%d'), Sale.saleDate <= datetime.strptime(toDate, '%Y-%m-%d'), Sale.drugId == drugId, Sale.userId==saler).all()
    elif fromDate and toDate and saler:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(User, (User.id == Sale.userId)).join(
            Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate >= datetime.strptime(fromDate, '%Y-%m-%d'), Sale.saleDate <= datetime.strptime(toDate, '%Y-%m-%d'), Sale.userId == saler).all()
    elif fromDate and toDate and drugId:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(User, (User.id == Sale.userId)).join(
            Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate >= datetime.strptime(fromDate, '%Y-%m-%d'), Sale.saleDate <= datetime.strptime(toDate, '%Y-%m-%d'), Sale.drugId == drugId).all()
    elif saler and drugId:
        datals=db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId==Drug.drugId)).join(User, (User.id==Sale.userId)).join(Employee, (Employee.employeeId==User.employeeId)).filter(Sale.userId==saler, Sale.drugId==drugId).all()
    elif fromDate and drugId:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(
            User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate >= datetime.strptime(fromDate, '%Y-%m-%d'), Sale.drugId == drugId).all()
    elif fromDate and saler:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(
            User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate >= datetime.strptime(fromDate, '%Y-%m-%d'), Sale.userId == saler).all()
    elif fromDate and toDate:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(
            User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate >= datetime.strptime(fromDate, '%Y-%m-%d'), Sale.saleDate <= datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif toDate and drugId:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(
            User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.drugId == drugId, Sale.saleDate <= datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif toDate and drugId:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(
            User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate <= datetime.strptime(toDate, '%Y-%m-%d'), Sale.userId == saler).all()
    elif drugId:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(
            Drug, (Sale.drugId == Drug.drugId)).join(User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.drugId == drugId).all()
    elif fromDate:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(
            User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate >= datetime.strptime(fromDate, '%Y-%m-%d')).all()
    elif toDate:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId == Drug.drugId)).join(
            User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).filter(Sale.saleDate <= datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif saler:
        datals=db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(Drug, (Sale.drugId==Drug.drugId)).join(User, (User.id==Sale.userId)).join(Employee, (Employee.employeeId==User.employeeId)).filter(Sale.userId==saler).all()
    else:
        datals = db.session.query(Sale.saleId, Drug.drugName, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate, Sale.billNo, Sale.userId, Employee.employeeName).join(
            Drug, (Sale.drugId == Drug.drugId)).join(User, (User.id == Sale.userId)).join(Employee, (Employee.employeeId == User.employeeId)).all()

    return render_template("admin/saleReport.html", data=datals)

@app.route('/byBillNo/<main>')
def byBillNo(main):
    billNo=0

    if main == '1':
        billNo = db.session.query(Sale.billNo).order_by(Sale.saleId.desc()).first()
        billNo=billNo[0]
    if main=='0':
        billNo=request.args.get('billNo')

    datals=db.session.query(Drug.drugName, Sale.saleId, Sale.drugPrice, Sale.drugQuantity, Sale.saleDate).join(Sale, (Sale.drugId==Drug.drugId)).filter(Sale.billNo==billNo).all()
    return render_template('admin/billData.html', data=datals, maxBill=billNo)


#drugs routes
@app.route('/storeDrug/<modification>/<drugId>', methods=['POST', 'GET'])
def storeDrug(modification, drugId):

    drug=Drug()
    form = StoreDrugForm()

    name=form.dname.data
    type=form.type.data
    Category=form.Category.data
    company=form.company.data
    barcode=form.barcode.data


    if form.validate_on_submit and modification == 'n':
        data=Drug.query.filter(func.lower(Drug.drugName)==func.lower(name)).all()
        if data:
            print(data)
            flash("duplicate")
            return redirect('drug')
        else:
            print('none')
            drug.store(name, type, company, Category, barcode)
            return redirect('/drug/None')
    elif form.validate_on_submit and modification == 'y' :
        drug.update(drugId, name, type, Category, company, barcode)

    return redirect('/drug/None')




@app.route('/', methods = ['GET'])
@app.route("/redirection")
@login_required
def redirection():
    role=db.session.query(UserRoles,Role.name).join(User,(User.id==UserRoles.user_id)).join(Role,(Role.id==UserRoles.role_id)).filter(User.id==current_user.id).all()[0][1]
    if role=='admin':
        return redirect (url_for('home'))
    elif role=='doctor':
        return redirect (url_for('docterView'))
    elif role=='receiption':
        return redirect (url_for('reciptionView'))
    elif role=='test':
        return redirect (url_for('LabView'))
    elif role=='purchase':
        return redirect (url_for('purchaseView'))

@app.route('/home', methods = ['GET'])
# @roles_required('admin')
def home():
   return render_template("admin/index.html")


@app.route('/drug/<drugId>', methods = ['GET'])
def drug(drugId):
    form = StoreDrugForm()
    decoding = Decoding()
    rout = '0'
    if drugId == 'None':
        rout = '0'
    else:
        rout = drugId
        data = Drug.query.get(rout)
        form.dname.data = data.drugName
        form.Category.data = data.categoryName
        form.company.data = data.companyName
        form.barcode.data = data.barcode


    form.type.choices = decoding.drugTypeNames()
    form.Category.choices = decoding.drugCategoryNames()
    form.company.choices = decoding.compnayNames()

    drug=Drug()
    data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).all()
    lower=9*10**12
    upper=10**13-1
    return render_template(("admin/drug.html"), dataList=data, code=random.randint(lower, upper), form = form, rout = rout)


@app.route('/generateBCR', methods=['POST'])
def generateBCR():

    drug=Drug()
    data=request.get_json()

    product=Drug.query.get(data);
    print(product.drugName)
    ean = barcode.get('ean13', str(product.barcode))
    filename=ean.save('static/'+product.drugName)

    return jsonify(result=(product.drugName))
    #return render_template('admin/printBCR.html', data=data, product=product, code=code)

@app.route('/drugFilter')
def drugFilter():
    drug=Drug()
    type=request.args.get('type')
    category=request.args.get('category')
    data=[]
    if type:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).filter(Drug.drugType==type).all()
    elif category:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).filter(Drug.categoryName==category).all()
    elif category and type:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).filter(Drug.categoryName==category and Drug.drugType==type).all()
    else:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).all()


    return render_template('admin/drug.html', dataList=data)

@app.route('/drugReport')
def drugReport():
    drug=Drug()
    type=request.args.get('type')
    category=request.args.get('category')
    data=[]
    if type:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).filter(Drug.drugType==type).all()
    elif category:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).filter(Drug.categoryName==category).all()
    elif category and type:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).filter(Drug.categoryName==category and Drug.drugType==type).all()
    else:
        data=db.session.query(Drug.drugId, Drug.drugName, Drug.barcode, DrugType.name.label('drugType'), Category.name.label('categoryName'), Company.name.label('companyName')).join(DrugType, (DrugType.id==Drug.drugType)).join(Category, (Category.id==Drug.categoryName)).join(Company, (Company.id==Drug.companyName)).all()

    return render_template('admin/drugReport.html', dataList=data)


@app.route('/updateDrug/<drugId>/<modification>')
def updateDrug(drugId, modification):
    if modification=='y':
        d=Drug()
        data=d.query.get(drugId)
        print(data.drugId)
        return render_template('admin/updateDrug.html', data=data)
    else:
        name=request.args.get('dname')
        type=request.args.get('type')
        Category=request.args.get('Category')
        company=request.args.get('company')
        barcode=request.args.get('barcode')
        if name and type and Category and company and barcode:
            drug=Drug()
            drug.update(drugId, name, type, company, Category, barcode)
            return redirect('drug')

    return redirect('drug')

@app.route('/removeDrug/<drugId>')
def removeDrug(drugId):
   drug=Drug()
   drug.delete(drugId)

   return redirect('admin/drug')




# lab routes
@app.route('/labTest', methods=['GET'])
def labTest():
    return render_template("admin/test.html")

@app.route('/testFilter')
def testFilter():
    patient = request.args.get('patient')
    doctor = request.args.get('doctor')
    testType = request.args.get('testType')
    testDate = request.args.get('testDate')
    status = request.args.get('status')
    data=[]

    form = TestFilterForm()
    decoding = Decoding()

    form.patient.choices = decoding.patientNames()

    form.doctor.choices = decoding.doctorNames()

    testTypes = db.session.query(TestType.Id, TestType.Name).all()
    form.testType.choices = testTypes

    if testType and testDate and status:
        data=db.session.query(Test.testId, Test.testDate, Test.action, TestType.Name, TestType.Amount).join(TestType, (Test.typeId==TestType.Id)).filter(Test.typeId==testType, Test.testDate >= datetime.strptime(testDate, '%Y-%m-%d'), Test.action==status).all()
    elif testType and testDate:
        data=db.session.query(Test.testId, Test.testDate, Test.action, TestType.Name, TestType.Amount).join(TestType, (Test.typeId==TestType.Id)).filter(Test.typeId==testType, Test.testDate >= datetime.strptime(testDate, '%Y-%m-%d')).all()
    elif testDate and status:
        data=db.session.query(Test.testId, Test.testDate, Test.action, TestType.Name, TestType.Amount).join(TestType, (Test.typeId==TestType.Id)).filter(Test.action == status, Test.testDate >= datetime.strptime(testDate, '%Y-%m-%d')).all()
    elif testType and status:
        data=db.session.query(Test.testId, Test.testDate, Test.action, TestType.Name, TestType.Amount).join(TestType, (Test.typeId==TestType.Id)).filter(Test.typeId==testType, Test.action==status).all()
    elif testType:
        data=db.session.query(Test.testId, Test.testDate, Test.action, TestType.Name, TestType.Amount).join(TestType, (Test.typeId==TestType.Id)).filter(Test.typeId==testType).all()
    else:
        data=db.session.query(Test.testId, Test.testDate, Test.action, TestType.Name, TestType.Amount).join(TestType, (Test.typeId==TestType.Id)).all()
    return render_template('admin/testFilter.html', data=data, form = form)



@app.route('/visitFilter', methods=["GET"])
def visitFilter():

    data=[]
    patient=request.args.get('patient')
    doctor=request.args.get('doctor')
    action=request.args.get('action')

    form = VisitFilterForm()
    decoding = Decoding()
    form.patient.choices = decoding.patientNames()
    form.doctor.choices = decoding.doctorNames()

    if patient and doctor and action:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).filter(Visit.patientId==patient, Visit.doctorId==doctor, Visit.action==action).all()
    elif patient and doctor:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).filter(Visit.patientId==patient, Visit.doctorId==doctor).all()
    elif patient and action:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).filter(Visit.patientId==patient, Visit.action==action).all()
    elif doctor and action:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).filter(Visit.doctorId==doctor, Visit.action==action).all()
    elif patient:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).filter(Visit.patientId==patient).all()
    elif doctor:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).filter(Visit.doctorId==doctor).all()
    elif action:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).filter(Visit.action==action).all()
    else:
        data=db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId==Patient.patientId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).all()
    return render_template('admin/visit.html', data=data, form = form)


@app.route('/visit', methods=['GET'])
def visit():
    data = db.session.query(Visit.visitId, Patient.patientName, Employee.employeeName, Visit.action).join(Patient, (Visit.patientId == Patient.patientId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).all()
    return render_template("admin/visit.html", data=data)


# this route is for admin thath show all registerd doctors
@app.route('/doctor/<doctorId>', methods = ['GET'])
def doctor(doctorId):
    a= doctorId
    print(a)
    form = DoctorForm()
    rout = '0'
    if doctorId == 'None':
       rout = '0'

    else:
       rout = doctorId
       data = Doctor.query.get(doctorId)


       form.room.data = data.roomNumber
       form.fee.data = data.fee
       form.profession.data = data.profession
       form.empNames.data = data.employeeId



    decoding = Decoding()
    form.empNames.choices = decoding.employeeNames()
    form.profession.choices = decoding.professionNames()
    jdata = db.session.query(Employee.employeeId, Employee.employeeName, Employee.phoneNumber, Employee.employeeEmail, Doctor.doctorId, Doctor.profession, Doctor.roomNumber, Doctor.fee, Job.name.label('employeeJob'), Profession.name.label('profession')).join(Doctor, (Doctor.employeeId == Employee.employeeId)).join(Job, (Employee.employeeJob==Job.id)).join(Profession, (Doctor.profession==Profession.id)).all()
    return render_template("admin/doctor.html", data=jdata, form = form, rout=rout)

@app.route('/storeDoctor/<modification>/<doctorId>', methods=['POST', 'GET'])
def storeDoctor(modification,doctorId ):
   form = DoctorForm()
   doctor = Doctor()
   name=form.empNames.data
   profession=form.profession.data
   room=form.room.data
   fee = form.fee.data


   if modification == 'n' and form.validate_on_submit:

        doctor.store(name, profession, room, fee)
        return redirect("/doctor/None")


   elif modification == 'y' and form.validate_on_submit:

       doctor.update(doctorId, name, profession, room, fee)
       return redirect("/doctor/None")







@app.route('/deleteDoctor/<doctorId>')
def deleteDoctor(doctorId):
   dr=Doctor()
   dr.delete(doctorId)

   return redirect('doctor')

@app.route('/updateDoctor/<doctorId>/<employeeId>/<modification>')
def updateDoctor(doctorId, employeeId, modification):
   data=[]
   dr=Doctor()
   rout=""
   if modification=='y':
      data = db.session.query(Employee.employeeId, Employee.employeeName, Employee.phoneNumber, Employee.employeeEmail, Doctor.doctorId, Doctor.profession, Doctor.roomNumber, Doctor.fee, Job.name.label('employeeJob'), Profession.name.label('profession')).join(Doctor, (Doctor.employeeId == Employee.employeeId)).join(Job, (Employee.employeeJob==Job.id)).join(Profession, (Doctor.profession==Profession.id)).filter(Doctor.doctorId==doctorId).all()[0]
   else:
      name=request.args.get('name')
      name=name.encode('utf-8')
      profession=request.args.get('profession')
      job = request.args.get('job')
      room = request.args.get('room')
      fee = request.args.get('fee')
      phone = request.args.get('phone')
      email = request.args.get('email')
      photo = request.args.get('photo')

      emp=Employee()
      emp.update(employeeId, name.encode('utf-8'), phone, ''.encode('utf-8'), 0, job, email, photo)
      dr.update(doctorId, employeeId, profession, room, fee)
      print(employeeId, name, phone, email, photo)
      print(doctorId, profession, room, fee)

      return redirect('admin/doctor')
   return render_template('admin/updateDoctor.html', data=data, rout=rout)

@app.route('/doctorByProfession/<report>')
def doctorByProfession(report):
   profession=request.args.get('profession')
   templateAddres='admin/doctor.html'
   form = DoctorReport()
   decoding = Decoding()
   form.profession.choices = decoding.professionNames()
   if report=='y':
        templateAddres = 'admin/doctorReport.html'

   if profession:
      data = db.session.query(Employee.employeeId, Employee.employeeName, Employee.phoneNumber, Employee.employeeEmail, Doctor.doctorId, Profession.name.label('profession'), Doctor.roomNumber, Doctor.fee).join(Doctor, (Doctor.employeeId == Employee.employeeId)).join(Job, (Job.id==Employee.employeeJob)).join(Profession, (Profession.id==Doctor.profession)).filter(Doctor.profession == profession).all()
   else:
      data = db.session.query(Employee.employeeId, Employee.employeeName, Employee.phoneNumber, Employee.employeeEmail, Doctor.doctorId, Profession.name.label('profession'), Doctor.roomNumber, Doctor.fee).join(Doctor, (Doctor.employeeId == Employee.employeeId)).join(Job, (Job.id==Employee.employeeJob)).join(Profession, (Profession.id==Doctor.profession)).all()

   return render_template(templateAddres, data=data,form = form )


# employees routes
@app.route('/employee/<salaryId>/<employeeId>', methods = ['GET'])
def employee(salaryId, employeeId):
   emp = Employee()
   decoding = Decoding()
   employeeForm = EmployeeForm()
   salaryForm = SalaryForm()


   if employeeId == 'None':

       employeeId = '0'
   else :
        employeeId = employeeId
        data = Employee.query.get(employeeId)

        employeeForm.name.data = data.employeeName.decode('utf-8')
        employeeForm.phone.data = data.phoneNumber
        employeeForm.job.data = data.employeeJob
        employeeForm.address.data = data.homeAddress.decode('utf-8')
        employeeForm.nic_no.data = data.NIC_No
        employeeForm.email.data = data.employeeEmail
   if salaryId == 'None':
       salaryId = '0'
   else :
       salaryId = salaryId
       data = Salary.query.get(salaryId)
       salaryForm.empNames.data = data.employeeID
       salaryForm.amount.data = data.amount
       salaryForm.month.data = data.month
       salaryForm.status.data = data.status




   salaryForm.empNames.choices = decoding.employeeNames()
   employeeForm.job.choices = decoding.jobNames()
   data = db.session.query(Employee.employeeId, Employee.employeeName, Employee.phoneNumber, Employee.employeeEmail, Employee.homeAddress, Doctor.doctorId, Profession.name.label('profession'), Job.name.label('employeeJob'), Doctor.roomNumber, Doctor.fee, Employee.NIC_No, Employee.employeePhoto).outerjoin(Doctor, (Doctor.employeeId == Employee.employeeId)).outerjoin(Job, (Job.id==Employee.employeeJob)).outerjoin(Profession, (Profession.id==Doctor.profession)).all()
   # print(dataList)
   dlist=db.session.query(Payment.visitId, Employee.employeeName, Doctor.fee, func.count(Visit.patientId).label('pCount')).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Employee.employeeId==Doctor.employeeId)).filter(Payment.testId==None).group_by(Payment.visitId).all()
   tlist=db.session.query(Payment.testId, TestType.Amount, TestType.Name, func.count(Visit.patientId).label('pCount')).join(Visit, (Payment.visitId==Visit.visitId)).join(Test, (Test.testId==Payment.testId)).join(TestType, (Test.typeId==TestType.Id)).filter(Payment.testId!=None).group_by(Payment.testId).all()
   salaryData=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).all()

   sumt=0
   sumt = [d.Amount*d.pCount for d in tlist]
   sumt=sum(sumt)
   sumd = [d.fee*d.pCount for d in dlist]
   sumd = sum(sumd)
   return render_template("admin/employee.html", dataList = data, dlist=dlist, tlist=tlist, sumt=sumt, sumd=sumd, employeeForm = employeeForm, salaryForm = salaryForm, employeeId = employeeId, salaryId = salaryId, salaryData = salaryData)

@app.route('/storeEmployee/<modification>/<employeeId>', methods = ['POST'])
def storeEmployee(modification,employeeId ):

   form = EmployeeForm()
   emp = Employee()

   name = form.name.data
   phone = form.phone.data
   job = form.job.data
   address = form.address.data
   nic_no = form.nic_no.data
   email = form.email.data
   print(name, phone, job, address, nic_no, email)


   if modification == 'n' and form.validate_on_submit:
        data=Employee.query.filter(Employee.phoneNumber==phone).all()
        if data:
            print(data)
            flash("duplicate")
            return redirect('employee/None/None')
        else:
            print()
            emp.store(name.encode('utf-8'), phone, address.encode('utf-8'), nic_no,job,email)
            return redirect('employee/None/None')
   elif modification == 'y' and form.validate_on_submit:
        emp.update(employeeId,name.encode('utf-8'), phone, address.encode('utf-8'),nic_no,job,email  )
        return redirect('employee/None/None')





@app.route('/removeEmp/<empId>')
def removeEmp(empId):
      emp=Employee()
      emp.delete(empId)
      return redirect('/admin/employee')



@app.route('/updateEmployee/<employeeId>/<modification>')
def updateEmployee(employeeId, modification):
    data=[]
    if modification=='y':
        emp=Employee()
        data=emp.query.get(employeeId)
    else:
        name = request.args.get('name')
        job = request.args.get('job')
        phone = request.args.get('phone')
        address = request.args.get('address')
        nic_no = request.args.get('nic_no')
        email = request.args.get('email')
        photo = request.args.get('photo')

        emp=Employee()
        emp.update(employeeId, name.encode('utf-8'), phone, address.encode('utf-8'), nic_no, job, email, photo)
        return redirect('employee')

    return render_template("admin/updateEmployee.html",dataList = data )

@app.route('/employeeByJob/<report>')
def employeeByJob(report):
   job=request.args.get('job')
   emp = Employee()
   decoding = Decoding()
   data=[]
   form = EmployeeReportForm()
   form.job.choices = decoding.jobNames()
   templateAddress='admin/employee.html'
   if report=='y':
       templateAddress='admin/employeeReport.html'
   if job:
      data = db.session.query(Employee.employeeId, Employee.employeeName, Employee.phoneNumber, Employee.employeeEmail, Employee.homeAddress, Doctor.doctorId, Profession.name.label('profession'), Job.name.label('employeeJob'), Doctor.roomNumber, Doctor.fee, Employee.NIC_No, Employee.employeePhoto).outerjoin(Doctor, (Doctor.employeeId == Employee.employeeId)).outerjoin(Job, (Job.id==Employee.employeeJob)).outerjoin(Profession, (Profession.id==Doctor.profession)).filter(Employee.employeeJob == job).all()
   else:
      data = db.session.query(Employee.employeeId, Employee.employeeName, Employee.phoneNumber, Employee.employeeEmail, Employee.homeAddress, Doctor.doctorId, Profession.name.label('profession'), Job.name.label('employeeJob'), Doctor.roomNumber, Doctor.fee, Employee.NIC_No, Employee.employeePhoto).outerjoin(Doctor, (Doctor.employeeId == Employee.employeeId)).outerjoin(Job, (Job.id==Employee.employeeJob)).outerjoin(Profession, (Profession.id==Doctor.profession)).all()

   return render_template(templateAddress, dataList=data, form = form)


@app.route('/storeSalary/<modification>/<salaryId>', methods=['POST'])
def storeSalary(modification, salaryId):
   form = SalaryForm()
   salary = Salary()
   empName = form.empNames.data
   amount = form.amount.data
   month = form.month.data
   status = form.status.data
   if form.validate_on_submit and modification =='n':
        salary.store(empName, month, amount, status)
        return redirect ('/employee/None/None')
   elif form.validate_on_submit and modification == 'y':
        salary.update(salaryId, empName, month, amount, status)
        return redirect ('/employee/None/None')







   return redirect('employee')

@app.route('/showSalary', methods=['GET', 'POST'])
def showSalary():
   try:
      salaryData=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).all()
      print(salaryData)
      return jsonify(salaryData)


   except Exception as e:
        print(str(e))

@app.route('/salaryReport')
def salaryReport():
    empId=request.args.get('emp')
    salaryDate=request.args.get('salaryDate')
    status=request.args.get('status')
    data=[]
    form = employee()
    employees = db.session.query(Employee.employeeId, Employee.employeeName).all()
    decoding=Decoding()
    form.emp.choices = decoding.employeeNames()
    if empId:
        data=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(
            Employee, (Salary.employeeID == Employee.employeeId)).filter(Salary.employeeID==empId).all()
    elif salaryDate:
        data=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).filter(Salary.month<=datetime.strptime(salaryDate, '%Y-%m-%d')).all()
    elif status:
        data=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).filter(Salary.status==status).all()
    elif empId and salaryDate:
        data = db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(
            Employee, (Salary.employeeID == Employee.employeeId)).filter(Salary.employeeID == empId, Salary.month <= datetime.strptime(salaryDate, '%Y-%m-%d')).all()
    elif empId and status:
        data = db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(
            Employee, (Salary.employeeID == Employee.employeeId)).filter(Salary.employeeID == empId, Salary.status==status).all()
    elif status and salaryDate:
        data=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).filter(Salary.month<=datetime.strptime(salaryDate, '%Y-%m-%d'), Salary.status==status).all()
    elif empId and salaryDate and status:
        data=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).filter(Salary.employeeId==empId, Salary.status==status, Salary.month<=datetime.strptime(salaryDate, '%Y-%m-%d')).all()
    else:
        data=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).all()

    return render_template('admin/salaryReport.html', data=data, form =form)

@app.route('/removeSalary/<salaryId>')
def removeSalary(salaryId):
   print(salaryId)
   salary=Salary()
   Salary.delete(salaryId)
   return redirect('employee')


@app.route('/updateSalary/<modification>/<salaryId>')
def updateSalary(salaryId, modification):
   salaryData=[]
   if modification=='n':
      salaryData=db.session.query(Salary.salaryId, Employee.employeeName, Salary.month, Salary.amount, Salary.status).join(Employee, (Salary.employeeID==Employee.employeeId)).filter(Salary.salaryId==salaryId).all()[0]
   else:
      empName = request.args.get('empNames')
      month = request.args.get('month')
      amount = request.args.get('amount')
      status = request.args.get('status')

      if empName and month and amount and status:
         emp = Employee()
         empID = db.session.query(Employee.employeeId).filter(
         Employee.employeeName == empName).all()
         empID = int(empID[0].employeeId)
         # print(type(empID[0].employeeId), empID[0].employeeId, int(empID[0].employeeId))
         salary = Salary()
         # print(salaryId, empID, empName, month, amount, status)
         Salary.update(salaryId, empID, month, amount, status)

         return redirect('/employee')

   return render_template('admin/updateSalary.html', data=salaryData)
   # print(salaryId, modification)

@app.route('/login')
def login():
   user=User()
   data=User.query.all()
   print(data)
   return "done"

# pateints routes
@app.route('/patient/<report>', methods = ['GET'])
def patient(report):
    templateAddress='admin/patient.html'

    if report=='y':
        templateAddress='admin/patientReport.html'

    gender=request.args.get('status')

    if gender:
        data=Patient.query.filter(Patient.gender==gender).all()
    else:
        p=Patient()
        data=p.show()

    return render_template(templateAddress, data=data)

@app.route('/deletePateint/<pateintId>')
def deletePateint(pateintId):
   p=Patient()
   p.delete(pateintId)

   return redirect('patient')


# sichness routes
@app.route('/sickness', methods = ['GET'])
def sickness():
   return render_template("admin/sickness.html")

@app.route('/clinicReport', methods = ['GET'])
def clinicReport():
    data=Drug.query.all()
    print(data)
    return render_template("admin/clinicReport.html")

# tests routes

@app.route('/test', methods = ['GET'])
def test():
   return render_template("admin/test.html")

@app.route('/showTest', methods = ['GET', 'POST'])
def showTest():
  datalist = db.session.query(Test.action, Patient.patientId, Patient.patientName, Doctor.doctorId,Employee.employeeName, func.count(Test.typeId).label('count'), Visit.visitId).filter(
  Visit.patientId == Patient.patientId).filter(Doctor.doctorId == Visit.doctorId ).filter(
  Employee.employeeId == Doctor.employeeId).filter(
  Test.typeId == TestType.Id).filter(Test.testId == Payment.testId).filter(Visit.visitId == Payment.visitId).filter(Payment.testId != None).group_by(Patient.patientId,Patient.patientName,Doctor.doctorId,Employee.employeeName, Visit.visitId, Test.action ).all()
  print(datalist)
  return render_template('Doctor/tests.html', datalist = datalist)

#user routes
def dec(item):
    return item.decode('utf-8')

@app.route('/user', methods = ['GET','POST'])
def user():
    form=Register()

    employee=Employee.query.with_entities(Employee.employeeId,Employee.employeeName).all()
    data=dict()
    i=1
    for emp in employee:
        data[emp.employeeId]=emp.employeeName.decode('utf-8')
        i+=1
    #data.employeeName.decode('utf-8')

    print (data.items())
    role=Role.query.with_entities(Role.name,Role.name)
    form.employee.choices=list(data.items())
    form.role.choices=role

    users=db.session.query(User.id, User.username,User.active, Role.name,Employee.employeeName).filter(User.id==UserRoles.user_id).filter(Role.id==UserRoles.role_id).filter(User.employeeId==Employee.employeeId).all()
    print(users)
    if form.validate_on_submit():
        user=User.query.filter(User.username==form.username.data).first()
        if user:
            flash("user is already created")
            return redirect("user")
        else:
            role=Role.query.filter(Role.name==form.role.data).first()
            if role:
                pass
            else:
                role=Role(name=form.role.data)
            user=User(employeeId=form.employee.data,username=form.username.data,password=user_manager.hash_password(form.password.data),active=form.active.data)
            user.roles=[role,]
            db.session.add(user)
            db.session.commit()
            flash("user is already created",'success')
            return redirect("user")
    return render_template("admin/user.html", form=form,users=users)


@app.route('/user/<uId>')
def removeUser(uId):
      user=User()
      user.delete(uId)
      flash("user deleted")
      return redirect(url_for("user"))

@app.route('/user/update/<uId>',methods=['GET','POST'])
def updateUser(uId):

    user=db.session.query(User).filter(User.id==uId).first()
    form=UpdateUserForm(active=user.active)
    role=db.session.query(Role.name).filter(Role.id==UserRoles.role_id).filter(UserRoles.user_id==uId).first()
    roles=Role.query.with_entities(Role.name,Role.name)
    form.role.choices=roles
    form.role.choices.default=role
    if form.validate_on_submit():
        user.active=form.active.data
        role=Role.query.filter(Role.name==form.role.data).first()
        user.roles=[role,]
        db.session.add(user)
        db.session.commit()
        flash("User updated successfully")
        return render_template ("admin/update_user.html",form=form, username=user.username)
    return render_template ("admin/update_user.html",form=form, username=user.username)

@app.route("/user/resetpass/<uId>",methods=['GET','POST'])
def resetpass(uId):
    user=db.session.query(User).filter(User.id==uId).first()
    form= ResetPassword()
    if form.validate_on_submit():
        user.password=user_manager.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password changed successfully')
        return render_template("admin/reset_password.html", form=form)

    return render_template("admin/reset_password.html", form=form)

@app.route('/pharmicyreport/<filter>', methods = ['GET'])
def pharmicyreport(filter):
    data=[]
    datals=[]
    sumt=[]
    datas=[]
    try:
        if filter=='n':

            data=db.session.query(Sale.drugId, Drug.drugName, func.sum(Sale.drugPrice).label('priceTotal'), func.sum(Sale.drugQuantity).label('qtyTotal'), func.sum(Sale.drugPrice*Sale.drugQuantity).label('Total')).join(Drug, (Sale.drugId==Drug.drugId)).group_by(Sale.drugId).all()
            datals=db.session.query(Purchase.drugId, Drug.drugName, func.sum(Purchase.drugPrice).label('priceTotal'), func.sum(Purchase.drugQuantity).label('qtyTotal'), func.sum(Purchase.drugPrice*Purchase.drugQuantity).label('Total')).join(Drug, (Purchase.drugId==Drug.drugId)).group_by(Purchase.drugId).all()
            sumt= db.session.query(func.sum(Purchase.drugPrice*Purchase.drugQuantity).label('pTotal')).all()[0], db.session.query(func.sum(Sale.drugPrice*Sale.drugQuantity).label('sTotal')).all()[0]

            datas = list(db.engine.execute(text("SELECT drugId, drugName, sum(sqty) as sTotal, sum(pqty) as pTotal, sum(pqty)-sum(sqty) as balance FROM ( SELECT e.drugId, e.drugName, sum(s.drugQuantity) as sqty, 0 as pqty FROM cms_tbl_sales as s join cms_tbl_drugs e on e.drugId=s.drugId group by e.drugId UNION SELECT e.drugId, e.drugName, 0 as sqty, sum(p.drugQuantity) as pqty FROM cms_tbl_purchases as p join cms_tbl_drugs e on p.drugId=e.drugId group by e.drugId ) x group by drugId, drugName").execution_options(autocommit=True)))

            # datap=db.session.query(Drug.drugId, Drug.drugName, func.sum(Purchase.drugQuantity).label('pTotal')).outerjoin(Purchase, (Purchase.drugId==Drug.drugId)).group_by(Drug.drugId).all()
            print(datas)
        else:
            fromDate=request.args.get('fromDate')
            toDate=request.args.get('toDate')
            if fromDate and toDate:
                data=db.session.query(Sale.drugId, Drug.drugName, func.sum(Sale.drugPrice).label('priceTotal'), func.sum(Sale.drugQuantity).label('qtyTotal'), func.sum(Sale.drugPrice*Sale.drugQuantity).label('Total')).join(Drug, (Sale.drugId==Drug.drugId)).group_by(Sale.drugId).filter(Sale.sellDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Sale.sellDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()
                datals=db.session.query(Purchase.drugId, Drug.drugName, func.sum(Purchase.drugPrice).label('priceTotal'), func.sum(Purchase.drugQuantity).label('qtyTotal'), func.sum(Purchase.drugPrice*Purchase.drugQuantity).label('Total')).join(Drug, (Purchase.drugId==Drug.drugId)).filter(Sale.sellDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Sale.sellDate<=datetime.strptime(toDate, '%Y-%m-%d')).group_by(Purchase.drugId).all()
                sumt= db.session.query(func.sum(Purchase.drugPrice*Purchase.drugQuantity).label('pTotal')).all()[0], db.session.query(func.sum(Sale.drugPrice*Sale.drugQuantity).label('sTotal')).filter(Sale.sellDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Sale.sellDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()[0]
                datas = list(db.engine.execute(text("SELECT drugId, drugName, sum(sqty) as sTotal, sum(pqty) as pTotal, sum(pqty)-sum(sqty) as balance FROM ( SELECT e.drugId, e.drugName, sum(s.drugQuantity) as sqty, 0 as pqty FROM cms_tbl_sales as s join cms_tbl_drugs e on e.drugId=s.drugId group by e.drugId UNION SELECT e.drugId, e.drugName, 0 as sqty, sum(p.drugQuantity) as pqty FROM cms_tbl_purchases as p join cms_tbl_drugs e on p.drugId=e.drugId group by e.drugId having p.purchaseDate>="+toDate+", p.purchaseDate<="+fromDate+") x group by drugId, drugName").execution_options(autocommit=True)))
            else:
                data=db.session.query(Sale.drugId, Drug.drugName, func.sum(Sale.drugPrice).label('priceTotal'), func.sum(Sale.drugQuantity).label('qtyTotal'), func.sum(Sale.drugPrice*Sale.drugQuantity).label('Total')).join(Drug, (Sale.drugId==Drug.drugId)).group_by(Sale.drugId).all()
                datals=db.session.query(Purchase.drugId, Drug.drugName, func.sum(Purchase.drugPrice).label('priceTotal'), func.sum(Purchase.drugQuantity).label('qtyTotal'), func.sum(Purchase.drugPrice*Purchase.drugQuantity).label('Total')).join(Drug, (Purchase.drugId==Drug.drugId)).group_by(Purchase.drugId).all()
                sumt= db.session.query(func.sum(Purchase.drugPrice*Purchase.drugQuantity).label('pTotal')).all()[0], db.session.query(func.sum(Sale.drugPrice*Sale.drugQuantity).label('sTotal')).all()[0]
                datas = list(db.engine.execute(text("SELECT drugId, drugName, sum(sqty) as sTotal, sum(pqty) as pTotal, sum(pqty)-sum(sqty) as balance FROM ( SELECT e.drugId, e.drugName, sum(s.drugQuantity) as sqty, 0 as pqty FROM cms_tbl_sales as s join cms_tbl_drugs e on e.drugId=s.drugId group by e.drugId UNION SELECT e.drugId, e.drugName, 0 as sqty, sum(p.drugQuantity) as pqty FROM cms_tbl_purchases as p join cms_tbl_drugs e on p.drugId=e.drugId group by e.drugId ) x group by drugId, drugName").execution_options(autocommit=True)))

    except Exception as e:
        print(e)

    return render_template("admin/report.html", data=data, datals=datals, sumt=sumt, datas=datas)



# purchases routes

@app.route('/purchase', methods = ['GET'])
def purchase():
   datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity, Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).all()
   return render_template("admin/purchase.html", data=datals)

@app.route('/purchaseByDate')
def purchaseByDate():
    drugId=request.args.get('drugId')
    fromDate=request.args.get('from')
    toDate=request.args.get('to')
    expireOn=request.args.get('expireOn')
    datals=[]

    if fromDate and toDate and drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d'), Purchase.drugId==drugId).all()
    elif fromDate and drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Purchase.drugId==drugId).all()
    elif fromDate and toDate:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif toDate and drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d'), Purchase.drugId==drugId).all()
    elif drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.drugId==drugId).all()
    elif fromDate:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d')).all()
    elif toDate:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif expireOn:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.drugExpirDate==datetime.strptime(expireOn, '%Y-%m-%d')).all()
    else:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity, Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).all()

    return render_template("admin/purchase.html", data=datals)

@app.route('/purchaseReport')
def purchaseReport():
    drugId=request.args.get('drugId')
    fromDate=request.args.get('from')
    toDate=request.args.get('to')
    expireOn=request.args.get('expireOn')
    datals=[]

    if drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.drugId==drugId).all()
    elif fromDate:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d')).all()
    elif toDate:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif fromDate and drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Purchase.drugId==drugId).all()
    elif fromDate and toDate:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif toDate and drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d'), Purchase.drugId==drugId).all()
    elif fromDate and toDate and drugId:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Purchase.purchaseDate<=datetime.strptime(toDate, '%Y-%m-%d'), Purchase.drugId==drugId).all()
    elif expireOn:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity,  Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.drugExpirDate>=datetime.strptime(expireOn, '%Y-%m-%d')).all()
    else:
        datals=db.session.query(Drug.drugName, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity, Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).all()

    return render_template("admin/purchaseReport.html", data=datals)



@app.route('/purchaseRig', methods=['GET'])
def purchaseRig():
   d=Drug()
   data=d.show()
   return render_template('admin/storePurchase.html', datals=data)

@app.route('/storePurchase', methods = ['GET'])
def storePurchase():

    name=request.args.get('pname')
    price=request.args.get('price')
    qty=request.args.get('qty')
    purchaseDate=request.args.get('purchaseDate')
    expiryDate=request.args.get('expiryDate')

    if name and price and qty and purchaseDate and expiryDate:
        purchase=Purchase()
        purchase.store(name, price, qty, purchaseDate, expiryDate)

    print(name, price, qty, purchaseDate, expiryDate)

    return redirect('/purchaseRig')


@app.route('/updatePurchase/<purchaseId>/<modification>')
def updatePurchase(purchaseId, modification):

    if modification=='y':
        datals=db.session.query(Drug.drugType, Purchase.purchaseId, Purchase.drugId, Purchase.drugPrice, Purchase.drugQuantity, Purchase.purchaseDate, Purchase.drugExpirDate).join(Purchase, (Drug.drugId==Purchase.drugId)).filter(Purchase.purchaseId==purchaseId).all()[0]
        print(purchaseId, modification, datals.drugType)
        d=Drug()
        data=d.show()
        return render_template('admin/purchaseUpdate.html', datals=datals, data=data)
    elif modification=='n':
        pname=request.args.get('pname')
        price=request.args.get('price')
        qty=request.args.get('qty')
        purchaseDate=request.args.get('purchaseDate')
        expiryDate=request.args.get('expiryDate')

        p=Purchase()
        p.update(purchaseId, pname, price, qty, purchaseDate, expiryDate)
        #print('wow', purchaseId, modification, pname, price, qty, purchaseDate, expiryDate)

    return redirect('purchase')

@app.route('/deletePurchase/<purchaseId>')
def deletePurchase(purchaseId):
    p=Purchase()
    p.delete(purchaseId)

    return redirect('admin/purchase')


#return routes
@app.route('/returnsale/<saleId>/<modification>', methods=['GET'])
def returnsale(saleId, modification):
    if modification=='y':
        s=Sale()
        data=s.query.get(saleId)
        return render_template('admin/return.html', data=data)
    else:
        s=Sale()
        drugId=s.query.get(saleId).drugId
        p=Purchase()
        price=p.query.filter(Purchase.drugId==drugId).all()[-1].drugPrice
        qty=request.args.get('qty')
        returnDate=datetime.now().strftime("%Y-%m-%d")

        r=Return()
        r.store(saleId, price, qty, returnDate)
        saleData=s.query.get(saleId)
        qty=float(saleData.drugQuantity)-float(qty)
        print(qty,saleData.drugQuantity)
        saleData.drugQuantity=qty
        s.update(saleData.saleId, saleData.drugId, saleData.drugPrice, saleData.drugQuantity, saleData.billNo)
    return redirect('saleReport')

@app.route('/returns')
def returns():
    data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).all()

    return render_template('admin/returns.html', data=data)

@app.route('/returnFilter')
def returnFilter():
    drugId=request.args.get('drugId')
    fromDate=request.args.get('from')
    toDate=request.args.get('to')
    data=[]

    if drugId:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).filter(Sale.drugId==drugId).all()
    elif fromDate:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).filter(Return.returnDate>=datetime.strptime(fromDate, '%Y-%m-%d')).all()
    elif toDate:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).filter(Return.returnDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif fromDate and drugId:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).filter(Return.returnDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Sale.drugId==drugId).all()
    elif fromDate and toDate:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).filter(Return.returnDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Return.returnDate<=datetime.strptime(toDate, '%Y-%m-%d')).all()
    elif toDate and drugId:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).filter(Return.returnDate>=datetime.strptime(toDate, '%Y-%m-%d'), Sale.drugId==drugId).all()
    elif fromDate and toDate and drugId:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).filter(Return.returnDate>=datetime.strptime(fromDate, '%Y-%m-%d'), Return.returnDate<=datetime.strptime(toDate, '%Y-%m-%d'), Sale.drugId==drugId).all()
    else:
        data=db.session.query(Drug.drugType, Drug.drugType, Return.returnId, Return.purchasePrice, Return.drugQuantity, Return.returnDate, Sale.billNo).join(Sale, (Sale.drugId==Drug.drugId)).join(Return, (Sale.saleId==Return.saleId)).all()

    return render_template("admin/returns.html", data=data)






# this route is for doctors which show patients which are assign to doctors

@app.route('/doctorView')
def doctorView():

    return render_template('Doctor/home.html')

@app.route('/confirmVisit/<visitId>')
def confirmVisit(visitId):
   try:
      visitPatient = db.session.query(Visit).filter(Visit.visitId == visitId).first()
      visitPatient.action = "visited"
      db.session.commit()
      return redirect('/unvisitedPatients')

   except e:
      print(e)

   return redirect('/unvisitedPatients')

@app.route('/rejectVisit/<visitId>')

def rejectVisit(visitId):
   try:
      visitPatient = db.session.query(Visit).filter(Visit.visitId == visitId).first()
      visitPatient.action = "unvisited"
      db.session.commit()
      return redirect('/visitedPatients')

   except e:
      print(e)

   return redirect('/visitedPatients')

@app.route('/unvisitedPatients', methods = ['GET'])
def unvisitedPatients():


    patientList = db.session.query(
     Visit.visitId, Patient.patientId, Patient.patientName, Patient.patientAge,
      Patient.gender, Patient.phoneNumber, Patient.visitDate
       ).filter(Visit.patientId == Patient.patientId).filter(Visit.doctorId == Doctor.doctorId).filter(Visit.doctorId == 1).filter(Visit.action == "unvisited").all()

    global value
    data=value
    value=0

    return render_template("Doctor/unvisited.html", patientList = patientList, value=data)

@app.route('/visitedPatients', methods = ['GET'])
def visitedPatients():


   patientList = db.session.query(
     Visit.visitId, Patient.patientId, Patient.patientName, Patient.patientAge,
      Patient.gender, Patient.phoneNumber, Patient.visitDate
       ).filter(Visit.patientId == Patient.patientId).filter(Visit.doctorId == Doctor.doctorId).filter(Visit.doctorId == 1).filter(Visit.action == "visited").all()

   return render_template("Doctor/visited.html", patientList = patientList)



# clinic routes

class AddTestForm(FlaskForm):

   Id = HiddenField('')
   name = StringField('نوم' , validators=[InputRequired(), length(min=2, max=20, message=' نوم باید د ۱۰ څخه تر ۲ پوری یی ')])
   amount = FloatField('مقدار' )


@app.route('/addTest', methods = ['GET', 'POST'])
def addTest():
   form = AddTestForm()
   testType = TestType()
   Id = form.Id.data

   if Id == 'none' and form.validate_on_submit():
      name = form.name.data
      amount = form.amount.data
      data=TestType.query.filter(func.lower(name)==func.lower(TestType.Name)).all()
      if data:
         print(data)
         flash("duplicate")
         return redirect('/addTest')
      else:
         testType.store(name, amount)
         print(Id)

         flash("Test Stored successfully")
         return redirect('/addTest')

   elif Id != None and form.validate_on_submit():


      name = form.name.data
      amount = form.amount.data
      testType.update(Id, name, amount)
      flash("Test updated successfully")

      return redirect('/addTest')

   def checkTestName(name):
      pass
   datalist = testType.show()
   form.Id.data = "none"
   return render_template("recieption/addTest.html", form = form, datalist = datalist)

@app.route('/updateTesType/<testTypId>', methods = ['GET', 'POST'])
def updateTesType(testTypId ):

   testResult = db.session.query(TestType).filter(TestType.Id == testTypId).first()

   form = AddTestForm()
   form.Id.data = testResult.Id
   form.name.data = testResult.Name
   form.amount.data = testResult.Amount
   testType = TestType()
   datalist = testType.show()
   return render_template('recieption/addTest.html', datalist = datalist , form = form)

@app.route('/removeTestype/<testTypId>', methods = ['GET', 'POST'])
def removeTestype(testTypId ):

   testType = TestType()
   testType.delete(testTypId)

   return redirect('addTest')



# thise route is for reception to store and show patients

@app.route('/addPatient', methods = ['GET', 'POST'])
def addPatient():
   form = AddPatientForm()
   patient = Patient()

   name = form.name.data
   patientId = form.Id.data

   age = form.age.data
   gender = form.gender.data
   phone = form.phone.data


   if patientId == 'none' and  form.validate_on_submit():
      data=Patient.query.filter(Patient.phoneNumber==phone).all()
      if data:
         print(data)
         flash("duplicate")
         return redirect('addPatient')
      else:
         patient.store(name.encode('utf-8'), age, gender,phone)
         flash("Patient Added successfully")
         return redirect('/addPatient')

   elif patientId != 'none' and  form.validate_on_submit():
      patient.update(patientId, name.encode('utf-8'), age, gender, phone)
      flash("Test updated successfully")

      return redirect('/addPatient')



   patientList = db.session.query(
   Patient.patientId, Patient.patientName, Patient.patientAge,
   Patient.gender, Patient.phoneNumber, Patient.visitDate
   ).all()

   form.Id.data = 'none'

   return render_template("recieption/addPatient.html",form = form, datalist = patientList  )
# this route is for reception to update patient

@app.route('/updatePatient/<patientId>', methods = ['GET', 'POST'])
def updatePatient(patientId):
   patientResult = db.session.query(Patient).filter(Patient.patientId == patientId).first()
   # print(testResult)
   form = AddPatientForm()
   form.Id.data = patientResult.patientId
   form.name.data = patientResult.patientName.decode('utf-8')
   form.age.data = patientResult.patientAge
   form.gender.data = patientResult.gender
   form.phone.data = patientResult.phoneNumber



   testType = TestType()
   patient = Patient()
   datalist = patient.show()
   return render_template('recieption/addPatient.html', datalist = datalist , form = form)


# this route is for reception to remove patient

@app.route('/removePatient/<patientId>', methods = ['GET'])
def removePatient(patientId):
   try:
      patient = Patient()
      patient.delete(patientId)
      return redirect('/addPatient')
   except IntegrityError:
      return ("all Ready exict")

   #    sys.exit("hellow")

   return redirect('/addPatient')


class TestTypeForm(FlaskForm):
   testId = HiddenField('')
   testName = SelectMultipleField("معاینات انتخاب کړی", id = "g", coerce=int)


# this route is for doctor to assign tests for patients

@app.route('/patientToLab/<patientID>', methods = ['GET'])

def patientToLab(patientID):

  form = TestTypeForm()
  form.testName.choices = [(row.Id, row.Name) for row in db.session.query(TestType.Id, TestType.Name)]
  form.testId.data = patientID

  return render_template("Doctor/assignToLab.html", form = form, patientID = patientID )


# this route is for recption to add test types

@app.route('/addPatientTest', methods = ['GET', 'POST'])
def addPatientTest():
   test = Test()
   payment = Payment()

   form = AddTestForm()

   patientID = request.args.get('testId')

   doctorID = 2
   testID = request.args.getlist('testName')
   result = db.session.query(Visit.visitId).filter(Visit.patientId == patientID).filter(Doctor.doctorId == 2).order_by(Visit.visitId.desc()).first()
   visitId = result.visitId

   countTest = 0
   for Id in testID:
      test.store(Id)
      countTest+=1
   # print(countTest)
   dbResultID = db.session.query(Test.testId).order_by(Test.testId.desc()).all()
   for d in dbResultID[:countTest]:

      payment.storeLabPayment(visitId, d.testId)


   return redirect('/visitedPatients')

@app.route('/testDetial/<visitId>')

def testDetial(visitId):
   testResult = db.session.query(Test.testId,Visit.visitId,Patient.patientName, TestType.Name).filter(Patient.patientId == Visit.patientId).filter(Test.typeId == TestType.Id).filter(Payment.testId == Test.testId).filter(Visit.visitId == visitId).filter(Visit.visitId == Payment.visitId).all()
   print(testResult)

   return render_template('Doctor/testDetial.html',testResult=testResult )

@app.route('/updateTest')
def updateTest():

   testId = request.args.get('testId')
   visitId = request.args.get('visitId')
   testTypeId = request.args.get('testTypeId')
   testId = db.session.query(Test).filter(Test.testId == Payment.testId).filter(Visit.visitId == Payment.visitId).filter(Test.typeId == TestType.Id).filter(Test.testId == testId).filter(Visit.visitId == visitId).first()
   testId.typeId = testTypeId
   db.session.commit()


   return redirect('/showTest')

@app.route('/removeTest<testId>/<visitId>')
def removeTest(testId,visitId):
   result = db.session.query(Test.testId).filter(Test.testId == Payment.testId).filter(Test.typeId == TestType.Id).filter(Test.testId == testId).filter(Visit.visitId == visitId).first()
   print(result.testId)
   test = Test()
   test.delete(result.testId)



   return redirect('/showTest')



# this route is for recption to show paid tests

@app.route('/testPayment', methods = ['GET'])
def testPayment():

   dataList = db.session.query(Payment.Id, Patient.patientName, Employee.employeeName, TestType.Name, TestType.Amount, Payment.amountStatus).filter(Payment.patientId == Patient.patientId).filter(Doctor.doctorId == Payment.doctorId).filter(Doctor.employeeId == Employee.employeeId).filter(Test.testId == Payment.testId).filter(Test.typeId== TestType.Id).filter(Payment.testId != None).all()

   return render_template("recieption/testPayment.html",dataList = dataList )


@app.route('/recieption/unpaidLab', methods = ['GET'])
def unpaidLab():

   dataList = db.session.query(Payment.Id, Patient.patientName, Employee.employeeName, TestType.Name, TestType.Amount, Payment.amountStatus).filter(Payment.patientId == Patient.patientId).filter(Doctor.doctorId == Payment.doctorId).filter(Doctor.employeeId == Employee.employeeId).filter(Test.testId == Payment.testId).filter(Test.typeId== TestType.Id).filter(Payment.testId != None).all()

# this route is for reception to pay unpaid tests


@app.route('/payLab', methods=['GET', 'POST'])
def payLab():

   jsonData = request.json
   visitId = jsonData['visitId']
   messeage = ''


   user = db.session.query(Payment).filter(Payment.visitId == visitId ).filter(Payment.testId != None).all()

   for u in user:
        u.amountStatus = "paid"
        db.session.commit()
        messeage = "paid"



   return jsonify(messeage)


@app.route('/unpayLab/<visitId>', methods=['GET', 'POST'])
def unpayLab(visitId):

   messeage = ''


   user = db.session.query(Payment).filter(Payment.visitId == visitId ).filter(Payment.testId != None).all()


   for u in user:
        u.amountStatus = "unpaid"
        db.session.commit()
        messeage = "unpaid"


   return redirect('showpaidLab')

@app.route('/a')
def a():
   return render_template('recieption/updateDocterpayment.html')


# payment reports

@app.route('/paymentFilter/<report>')
def paymentFilter(report):
    data=[]
    patientId = request.args.get('patient')
    doctorId = request.args.get('doctor')
    paymentdate = request.args.get('date')
    status = request.args.get('status')

    form = PayemntFilterForm()
    decoding = Decoding()
    form.patient.choices = decoding.patientNames()
    print(form.patient.choices)

    form.doctor.choices = decoding.doctorNames()

    if patientId and doctorId and paymentdate and status:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None, Visit.patientId == patientId, Visit.doctorId == doctorId, Payment.amountStatus == status, Payment.date >= datetime.strptime(paymentdate, '%Y-%m-%d')).all()
    elif patientId and doctorId and paymentdate:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None, Visit.patientId==patientId, Visit.doctorId==doctorId, Payment.date>=datetime.strptime(paymentdate, '%Y-%m-%d')).all()
    elif patientId and doctorId:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None, Visit.patientId==patientId, Visit.doctorId==doctorId).all()
    elif patientId:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None, Visit.patientId == patientId).all()
    elif doctorId:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None, Visit.doctorId == doctorId).all()
    elif paymentdate:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None, Payment.date >= datetime.strptime(paymentdate, '%Y-%m-%d')).all()
    elif status:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None, Payment.amountStatus == status).all()
    else:
        data = db.session.query(Payment.Id, Patient.patientName, Payment.date, Doctor.fee, Payment.amountStatus, Payment.discount, Employee.employeeName).join(Visit, (Payment.visitId == Visit.visitId)).join(Doctor, (Visit.doctorId == Doctor.doctorId)).join(Employee, (Doctor.employeeId == Employee.employeeId)).join(Patient, (Visit.patientId == Patient.patientId)).filter(Payment.testId==None).all()

    return render_template('admin/doctorPayment.html', data = data, form = form)


@app.route('/testPaymentFilter/<report>')
def testPaymentFilter(report):
    data=[]
    patientId = request.args.get('patient')
    testId = request.args.get('test')
    paymentdate = request.args.get('date')
    status = request.args.get('status')
    decoding = Decoding()

    form = TestPayemntFilterForm()
    form.patient.choices = decoding.patientNames()
    form.test.choices = decoding.testNames()

    if patientId and testId and paymentdate and status:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Visit.patientId == patientId, Test.typeId == testId, Payment.amountStatus == status, Payment.date >= datetime.strptime(paymentdate, '%Y-%m-%d')).all()
    elif patientId and testId and paymentdate:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Visit.patientId==patientId, Test.typeId ==testId, Payment.date>=datetime.strptime(paymentdate, '%Y-%m-%d')).all()
    elif patientId and testId and status:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Visit.patientId==patientId, Test.typeId ==testId, Payment.amountStatus==status).all()
    elif patientId and testId:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Visit.patientId==patientId, Test.typeId ==testId).all()
    elif testId and status:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Test.typeId ==testId, Payment.amountStatus==status).all()
    elif patientId and status:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Visit.patientId==patientId, Payment.amountStatus==status).all()
    elif patientId:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Visit.patientId==patientId).all()
    elif paymentdate:
        print('sdfsdf')
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Payment.date == datetime.strptime(paymentdate, '%Y-%m-%d')).all()
    elif testId:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Test.typeId == testId).all()
    elif status:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Payment.amountStatus == status).all()
    else:
        data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).all()


    return render_template('admin/testPayment.html', data=data, form = form)

class doctorPayment(FlaskForm):

   patientID = HiddenField("")
   doctorName = SelectField(" ډاکټر انتخاب کړی ", id = "g", coerce=int)


# this route is for recption to assign patients for doctors

@app.route('/reperTodoctor/<patientID>', methods = ['GET'])
def reperTodoctor(patientID):

   form = doctorPayment()
   decoding = Decoding()
   form.patientID.data = patientID
   form.doctorName.choices = decoding.doctorNames()

   return render_template("recieption/reperToDoctor.html", form = form)

# this route is for resiption to add doctor payment

@app.route('/adddoctorPayment', methods = ['POST'])
def adddoctorPayment():
   jsonData = request.json
   patientID = jsonData['patientId']
   doctorID = jsonData['doctorId']



   visit = Visit()
   payment = Payment()
   print(patientID,doctorID )
   visit.store(patientID,doctorID)
   visit = db.session.query(Visit.visitId).filter( Visit.patientId ==patientID ).filter(Visit.doctorId ==doctorID).order_by(Visit.visitId.desc()).first()
   payment.storeDoctorPayment(visit.visitId)

   return jsonify('hello')


@app.route('/updateDoctorPayment', methods = ['POST', 'GET'])
def updateDoctorPayment():
   visit = Visit()
   paymentId = request.args.get('paymentId')
   doctorId = request.args.get('doctorId')
   visitId = request.args.get('visitId')

   visit.update(visitId,doctorId )
   print(paymentId, doctorId)
   return redirect('/showDoterPayment')

@app.route('/updateLabPayment', methods = ['POST', 'GET'])
def updateLabPayment():
   paymentId = request.args.get('paymentId')
   doctorId = request.args.get('doctorId')
   payment = Payment()
   payment.updateDoctorPayment(paymentId, doctorId)
   return redirect('/showDoterPayment')


# this route is for recption to show paid payment

@app.route('/showDoctorPayment')
def showDoterPayment():
   dataList = db.session.query( Payment.Id, Visit.visitId ,Patient.patientName, Employee.employeeName, Doctor.fee).filter(Visit.visitId == Payment.visitId).filter(Visit.doctorId == Doctor.doctorId).filter(Visit.patientId == Patient.patientId).filter(Doctor.employeeId == Employee.employeeId).filter(Payment.testId == None).all()
   return render_template('recieption/showDoctorpayment.html', dataList = dataList)

@app.route('/deleteDoctorPayment/<paymentId>')
def deleteDoctorPayment(paymentId):
   visit = Visit()
   visit.delete(paymentId)

   return redirect('/showDoterPayment')

@app.route('/deleteLabPayment/<paymentID>')
def deleteLabPayment(paymentID):
   payment = Payment()
   payment.delete(paymentID)

   return redirect('/showLabPayment')



# ajax route

@app.route('/getpayReport' , methods=['GET', 'POST'])
def getpayReport():
   ID = request.json


   result = db.session.query(Payment.Id, Doctor.doctorId, Patient.patientName, Employee.employeeName ).filter(Payment.patientId == Patient.patientId, Doctor.employeeId == Employee.employeeId).filter(Payment.doctorId == Doctor.doctorId).filter(Payment.Id == ID).first()

   return (jsonify(result))


# this route is for reception to show paid tests


@app.route('/showpaidLab')
def showpaidLab():
   datalist = db.session.query(Patient.patientId, Patient.patientName, Doctor.doctorId,Employee.employeeName, func.count(Test.typeId).label('count'),func.sum(TestType.Amount).label('Total'),Payment.amountStatus, Visit.visitId).filter(
   Visit.patientId == Patient.patientId).filter(Doctor.doctorId == Visit.doctorId ).filter(
   Employee.employeeId == Doctor.employeeId).filter(
   Test.typeId == TestType.Id).filter(Visit.visitId == Payment.visitId).filter(Test.testId == Payment.testId).filter(Payment.testId != None).filter(Payment.amountStatus == 'paid').group_by(Patient.patientId,Patient.patientName,Doctor.doctorId,Employee.employeeName,Payment.amountStatus, Visit.visitId ).all()

   return render_template('recieption/paidLab.html', dataList = datalist)

@app.route('/showunpaidLab/<filter>')
def showunpaidLab(filter):
   datalist = ''
   if filter == 'n':
    datalist = db.session.query(Patient.patientId, Patient.patientName, Doctor.doctorId,Employee.employeeName, func.count(Test.typeId).label('count'),func.sum(TestType.Amount).label('Total'),Payment.amountStatus, Visit.visitId, Payment.date).filter(
    Visit.patientId == Patient.patientId).filter(Doctor.doctorId == Visit.doctorId ).filter(
    Employee.employeeId == Doctor.employeeId).filter(
    Test.typeId == TestType.Id).filter(Visit.visitId == Payment.visitId).filter(Test.testId == Payment.testId).filter(Payment.testId != None).filter(Payment.amountStatus == 'unpaid').group_by(Patient.patientId,Patient.patientName,Doctor.doctorId,Employee.employeeName,Payment.amountStatus, Visit.visitId, Payment.date ).all()
   else:
    visitId = request.args.get('visitId')

    datalist = db.session.query(Patient.patientId, Patient.patientName, Doctor.doctorId,Employee.employeeName, func.count(Test.typeId).label('count'),func.sum(TestType.Amount).label('Total'),Payment.amountStatus, Visit.visitId, Payment.date).filter(
    Visit.patientId == Patient.patientId).filter(Doctor.doctorId == Visit.doctorId ).filter(
    Employee.employeeId == Doctor.employeeId).filter(
    Test.typeId == TestType.Id).filter(Visit.visitId == Payment.visitId).filter(Test.testId == Payment.testId).filter(Payment.testId != None).filter(Payment.amountStatus == 'unpaid').group_by(Patient.patientId,Patient.patientName,Doctor.doctorId,Employee.employeeName,Payment.amountStatus, Visit.visitId, Payment.date ).filter(Visit.visitId == visitId).all()


   return render_template('recieption/unpaidLab.html', dataList = datalist)

@app.route('/tests/<visitId>')
def tests(visitId):
    form=TestFilterForm()
    data = db.session.query(Payment.Id, Patient.patientName, TestType.Name, Payment.date, TestType.Amount, Test.action, Payment.amountStatus, Payment.discount).join(Test, (Payment.testId==Test.testId)).join(TestType, (Test.typeId==TestType.Id)).join(Visit, (Payment.visitId==Visit.visitId)).join(Doctor, (Visit.doctorId==Doctor.doctorId)).join(Employee, (Doctor.employeeId==Employee.employeeId)).join(Patient, (Visit.patientId==Patient.patientId)).filter(Payment.visitId==visitId).all()
    return render_template('admin/testFilter.html', data=data, form=form)

# this route is for reseption to print doctor bill for patient

@app.route('/getpatientReport', methods = ['POST'])
def refresh():
   data = request.json
   patientID = data['patientID']
   doctorID = data['doctorID']
   print(doctorID)
   datalist = db.session.query(Patient.patientId,Patient.patientName, Patient.patientAge, Patient.gender,Patient.visitDate, Employee.employeeName, Doctor.fee, Doctor.roomNumber).filter(Patient.patientId == patientID , Doctor.employeeId == Employee.employeeId, Doctor.doctorId == doctorID , Employee.employeeId == Doctor.employeeId).all()
   print(datalist)

   return jsonify(datalist)

# this route is for recption to print bill for test of patient
@app.route('/getLabReport', methods = ['POST'])
def getLabReport():
   paymentID = request.json
   dataList = db.session.query(Patient.patientId,Test.testId,Patient.patientAge,Patient.gender,Patient.visitDate,Patient.patientName, Employee.employeeName, TestType.Name, TestType.Amount ).filter(Payment.patientId == Patient.patientId).filter(Doctor.doctorId == Payment.doctorId).filter(Doctor.employeeId == Employee.employeeId).filter(Test.testId == Payment.testId).filter(Test.typeId== TestType.Id).filter(Payment.Id == 4).all()
   # print(datalist)
   # datalist = datalist.patientId

   return jsonify(dataList)

@app.route('/getTestReport', methods = ['POST', 'GET'])
def getTestReport():
   b = request.json
   testId = b['testId']
   visitId = b['visitId']

   testTypeId = db.session.query(TestType.Id).filter().filter(Test.typeId == TestType.Id).filter(Payment.testId == Test.testId).filter(Visit.visitId == visitId).filter(Visit.visitId == Payment.visitId).filter(Test.testId == testId).all()

   return jsonify(testTypeId)

@app.route('/getTestPayment', methods = ['POST', 'GET'])

def getTestPayment():
   visitId = request.json

   testPaymentResult = db.session.query(TestType.Name, TestType.Amount).filter(Test.typeId == TestType.Id).filter(Visit.visitId == Payment.visitId).filter(Payment.visitId == visitId).filter(Test.testId == Payment.testId).all()

   return jsonify(testPaymentResult)



@app.route('/LabView/<filter>', methods = ['GET'])
def LabView(filter):
   datalist = ''
   if filter == 'n':
        datalist = db.session.query( Test.action ,Patient.patientId, Patient.patientName, Doctor.doctorId,Employee.employeeName, func.count(Test.typeId).label('count'), Visit.visitId).filter(
        Visit.patientId == Patient.patientId).filter(Doctor.doctorId == Visit.doctorId ).filter(
        Employee.employeeId == Doctor.employeeId).filter(
        Test.typeId == TestType.Id).filter(Test.testId == Payment.testId).filter(Visit.visitId == Payment.visitId).filter(Payment.testId != None).group_by(Test.action,Patient.patientId,Patient.patientName,Doctor.doctorId,Employee.employeeName, Visit.visitId ).all()
   else:
        visitId = request.args.get('visitId')
        datalist = db.session.query( Test.action ,Patient.patientId, Patient.patientName, Doctor.doctorId,Employee.employeeName, func.count(Test.typeId).label('count'), Visit.visitId).filter(
        Visit.patientId == Patient.patientId).filter(Doctor.doctorId == Visit.doctorId ).filter(
        Employee.employeeId == Doctor.employeeId).filter(
        Test.typeId == TestType.Id).filter(Test.testId == Payment.testId).filter(Visit.visitId == Payment.visitId).filter(Payment.testId != None).group_by(Test.action,Patient.patientId,Patient.patientName,Doctor.doctorId,Employee.employeeName, Visit.visitId ).filter(Visit.visitId == visitId).all()
   return render_template("Lab/LabView.html",datalist = datalist )


@app.route('/testAction<visitId>/<action>', methods = ['GET', 'POST'])
def testAction(visitId, action):
    print(234)
    user = db.session.query(Test).filter(Test.testId == Payment.testId ).filter(Payment.visitId == visitId ).filter(Payment.testId != None).all()
    if action == "y":
      for u in user:
         u.action = "tested"
         db.session.commit()
         messeage = "paid"
    else:
        for u in user:
         u.action = "untested"
         db.session.commit()
         messeage = "unpaid"
    return redirect("LabView/n")


@app.route('/testDetialForLab/<visitId>')

def testDetialForLab(visitId):
   testResult = db.session.query(Test.testId,Visit.visitId,Patient.patientName, TestType.Name).filter(Patient.patientId == Visit.patientId).filter(Test.typeId == TestType.Id).filter(Payment.testId == Test.testId).filter(Visit.visitId == visitId).filter(Visit.visitId == Payment.visitId).all()
   print(testResult)

   return render_template('Lab/testDetial.html',testResult=testResult )

@app.route('/recieptionView', methods = ['GET'])
def recieptionView():
   return render_template("recieption/home.html")


@app.route('/getdoctorName', methods = ['POST', 'GET'])
def getdoctorName():
   a = db.session.query(Doctor.doctorId.label('id') , Employee.employeeName.label('text')).filter(Employee.employeeId == Doctor.doctorId).all()
   return jsonify(a)


@app.route('/testNames', methods = ['POST', 'GET'])
def testNames():

   testNameResult = db.session.query(TestType.Id.label('id'), TestType.Name.label('text')).all()

   return jsonify(testNameResult)


# view for saler
@app.route('/saleDrug')
def saleDrug():
   return render_template('saler/Sale.html')

# view for purchaser

@app.route('/purchaseView')
def purchaseView():
   return render_template('purchaser/purchase.html')


# ajax requests


@app.route('/getEmployeeNames', methods = ['GET','POST'])
def getEmployeeNames():
    employee = Employee()
    empList = db.session.query(Employee.employeeId.label('id'), Employee.employeeName.label('text')).all()
    data=dict(empList)
    i=1
    for emp in employee:
        data[i]=emp.employeeName.decode('utf-8')
        i+=1

    return jsonify(list(data.items()))

@app.route('/getPatientNames', methods = ['GET', 'POST'])
def getPatientNames():
   try:
      patient = Patient()
      patientNames = db.session.query(Patient.patientId.label('id'), Patient.patientName.label('text')).all()
      return jsonify(patientNames)


   except Exception as e:
      print(str(e))



@app.route('/getPropeesions', methods = ['GET','POST'])
def getPropeesions():
    employee = Employee()
    professions = db.session.query(Employee.employeeId.label('id'), Employee.employeeJob.label('text')).all()

    return jsonify(professions)


@app.route('/getdrugNames', methods = ['GET','POST'])
def getdrugNames():

    drugNames = db.session.query(Drug.drugId.label('id'), Drug.drugName.label('text')).all()
    print(drugNames)

    return jsonify(drugNames)

@app.route('/getdrugType', methods = ['GET','POST'])
def getdrugType():

    drugTypes = db.session.query(DrugType.id.label('id'), DrugType.name.label('text')).all()


    return jsonify(drugTypes)

@app.route('/getdrugCategory', methods = ['GET','POST'])
def getdrugCategory():

    drugCategories = db.session.query(Category.id.label('id'), Category.name.label('text')).all()


    return jsonify(drugCategories)

@app.route('/getdrugCompany', methods = ['GET','POST'])
def getdrugCompany():

    drugCompanies = db.session.query(Company.id.label('id'), Company.name.label('text')).all()


    return jsonify(drugCompanies)

@app.route('/getsoldDrugNames', methods = ['GET','POST'])
def getsoldDrugNames():

    soldDrugs = db.session.query(Drug.drugId.label('id'), Drug.drugName.label('text')).distinct(Sale.drugId).filter(Drug.drugId == Sale.drugId).all()


    return jsonify(soldDrugs)

@app.route('/getDrugTypes', methods = ['GET','POST'])
def getDrugTypes():

    drugTypes = db.session.query(DrugType.id.label('id'), DrugType.name.label('text')).all()


    return jsonify(drugTypes)


@app.route('/getPurchasedDrugNames', methods = ['GET','POST'])
def getPurchasedDrugNames():

    PurchasedDrugs = db.session.query(Drug.drugId.label('id'), Drug.drugName.label('text')).distinct(Purchase.drugId).filter(Drug.drugId == Purchase.drugId).all()


    return jsonify(PurchasedDrugs)
@app.route("/backup/<type>")
def backup(type):
    if type=='daily':
        pwd='fsahim'
        cmd='automysqlbackup'
        if not (call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)):
            flash("Backed up successfully", 'success')
        else:
            flash("Error in backup process", 'danger')
        return render_template("admin/backup.html")
    return render_template("admin/backup.html")



@app.route('/dynamicStore', methods = ['GET','POST'])
def storeType():

    drugType = DrugType()
    category = Category()
    company = Company()
    data = request.json
    tableType = data['type']
    value = data['newValue']

    if tableType == 'type':
        drugType.store(value)
        getType = db.session.query(DrugType.id, DrugType.name).filter(DrugType.name == value).first()

        return jsonify(getType)

    elif tableType == 'Category':
        category.store(value)
        getCateogry = db.session.query(Category.id , Category.name).filter(Category.name == value).first()
        return jsonify(getCateogry)

    elif tableType == 'Company':
        company.store(value)
        getcompany = db.session.query(Company.id , Company.name).filter(Company.name == value).first()
        return jsonify(getcompany)
    elif tableType == 'job':
        job = Job()
        job.store(value)
        getJob = db.session.query(Job.id, Job.name).order_by(Job.id.desc()).first()
        return jsonify(getJob)

    elif tableType == 'profession':
        profession = Profession()
        profession.store(value)
        getProfession = db.session.query(Profession.id, Profession.name).order_by(Profession.id.desc()).first()
        return jsonify(getProfession)





@app.route('/b')
def b():
    return render_template('admin/dd.html')

@app.route('/checkForPatient')
def checkForPatient():

   pass
@app.route('/stock', methods=['POST'])
def stock():
    sumt=db.session.query(Drug.drugId, Drug.drugName, func.sum(Purchase.drugQuantity).label('pTotal'), func.sum(Sale.drugQuantity).label('sTotal')).outerjoin(Purchase, (Purchase.drugId==Drug.drugId)).outerjoin(Sale, (Sale.drugId==Drug.drugId)).group_by(Drug.drugId).all()
    #print((sumt[0].pTotal!=None if sumt[0].pTotal else 0)-(sumt[0].sTotal!=None if sumt[0].sTotal else 0))

    return jsonify(result=sumt)



    return jsonify(result=data)
if __name__ == "__main__":

   Bootstrap(app)
   app.config['SECRET_KEY'] = 'TYTYTYT'
   app.debug = True
   app.run()
