import xmlrpc.client
import json
from flask import Flask, request, render_template
from flask_cors import CORS
from datetime import datetime
import time

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})
url = "http://localhost:8069"
db = "project"

#################### Vue JS  link ##################
@app.route("/",methods=["GET"])
def index():
	return render_template("index.html")

@app.route("/list",methods=["GET"])
def show():
	return render_template("list.html")

@app.route("/create",methods=["GET"])
def createe():
	return render_template("create.html")

@app.route("/detail/<id>",methods=["GET"])
def detail(id):
	return render_template("detail.html")
@app.route("/update/<id>",methods=["GET"])
def update(id):
	return render_template("update.html")


######################################################## API LINK ########################

######################################################## Auth ########################
@app.route("/auth",methods=["POST"])
def auth():
	common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
	uid = common.authenticate(db,request.json["username"],request.json["password"],{})
	if not uid:
		return "Erreur", 400
	return str(uid) 

####################################################  List employee  ##########################################
@app.route("/api/employees",methods=['POST'])
def achats():
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		res = models.execute_kw(db,request.json["uid"],request.json["password"],"hr.employee","search_read",[[]],
		{"fields":["id","display_name","work_phone","gender","work_email","work_location","image_medium"]}
		)
		return json.dumps(res)
	except:
		print("Erreur")
		return "Erreur",400

#################################################### Create employee   ##########################################
@app.route("/api/create",methods=['POST'])
def create():
	try:
		models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
		create = models.execute_kw(db,request.json["uid"],request.json["password"],'hr.employee', 'create', [{
			'name': request.json["name"],
			'image_medium': request.json["image"],
			'gender': request.json["gender"],
			'work_email':request.json["email_work"],
			'department_id': int(request.json["departement"]),
			'job_id': int(request.json["job_postion"]),
			'resource_calendar_id': int(request.json["work_hours"]),
			'address_id':int(request.json["work_adress"]),
			'address_home_id':int(request.json["work_adress"]),
			'birthday': request.json["birthday"],
			'work_phone': request.json["mobile_work"],
			'place_of_birth': request.json["country"],
			'work_location': "Building 1, Second Floor",
			#'emergency_phone': request.json["personal_phone"],
			#'mobile_phone': request.json["uid"],

		}])

		return render_template("index.html")
	except:
		return "Error",400		
#################################################### Update employee   ##########################################
@app.route("/api/update/<int:_id>",methods=['POST'])
def updatee(_id):
	try:
		models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
		create = models.execute_kw(db,request.json["uid"],request.json["password"],'hr.employee', 'write', [[_id], {
			'name': request.json["name"],
			'image_medium': request.json["image"],
			'gender': request.json["gender"],
			'work_email':request.json["email_work"],
			'department_id': int(request.json["departement"]),
			'job_id': int(request.json["job_postion"]),
			'resource_calendar_id': int(request.json["work_hours"]),
			'address_id':int(request.json["work_adress"]),
			'address_home_id':int(request.json["work_adress"]),
			'birthday': request.json["birthday"],
			'work_phone': request.json["mobile_work"],
			'place_of_birth': request.json["country"],
			'work_location': "Building 1, Second Floor",
			#'emergency_phone': request.json["personal_phone"],
			#'mobile_phone':,

		}])

		return render_template("index.html")
	except:
		return "Error",400		
################################# Get one employee  #####################################
@app.route("/api/getEmployee",methods=['POST'])
def getOrder():
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		order = models.execute_kw(db,request.json["uid"],request.json["password"],
		'hr.employee','search_read',
		 [[['id','=',request.json["oid"]]]],
		{}
		)
		return json.dumps(order)
	except:
		return "Erreur",400






############################## cancel ##############################

@app.route("/api/cancel/<int:_id>",methods=['POST'])
def cancel(_id):
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		res = models.execute_kw(db,request.json["uid"],request.json["password"],"hr.employee","write",[[_id],{"state":"cancel"}])
		return "Canceled",200
	except:
		print("Erreur")
		return "Erreur",400
############################## Delete ##############################

@app.route("/api/delete/<int:_id>",methods=['POST'])
def delete(_id):
	cancel(_id)
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		res = models.execute_kw(db,request.json["uid"],request.json["password"],"hr.employee","unlink",[[_id]])
		return "Employee Deleted ",200
	except:
		print("Erreur")
		return "Erreur",400


############################### Helper Api ###################

################################# Get Company #####################################
@app.route("/api/getCompany",methods=['POST'])
def getCompany():
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		partner = models.execute_kw(
		db,request.json["uid"],request.json["password"],
		'res.partner', 'search_read', [[]],
		{"fields":['partner_id','name']}
		)
		return json.dumps(partner)
	except :
		print("Erreur")
		return "Erreur",400
################################# Get Departement #####################################
@app.route("/api/getDepartement",methods=['POST'])
def getDepartement():
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		
		departement = models.execute_kw(db,request.json["uid"],request.json["password"],"hr.department","search_read",[[]],
		{
			"fields":["id","display_name"]
		})
		return json.dumps(departement)
	except :
		print("Erreur")
		return "Erreur",400
################################# Get Departement #####################################
@app.route("/api/getJobs",methods=['POST'])
def getJobs():
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		
		job = models.execute_kw(db,request.json["uid"],request.json["password"],"hr.job","search_read",[[]],
		{
			"fields":["id","name"]
		})

		return json.dumps(job)
	except :
		print("Erreur")
		return "Erreur",400
################################# Get Country #####################################
@app.route("/api/getCountry",methods=['POST'])
def getCountry():
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		
		job = models.execute_kw(db,request.json["uid"],request.json["password"],"res.country",
		"search_read",[[]],
		{
			"fields":["id","name"]
		}) 

		return json.dumps(job)
	except :
		print("Erreur")
		return "Erreur",400


if __name__ == "__main__":
	app.run()
