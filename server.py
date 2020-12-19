import xmlrpc.client
import json
from flask import Flask, request, render_template
from flask_cors import CORS

'''
 global variable needed for the api
'''
url = "http://localhost:8069"
db = "projet"


'''
 initializing the app and the CORS middleware
'''
app = Flask(__name__)
CORS(app)


'''
 helper functions
'''
# --------------------------------
def call(args,err):
	models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
	try:
		res = models.execute_kw(db,request.json["uid"],request.json["password"],*args)
		return json.dumps(res),200
	except Exception as e:
		print(e)
		return json.dumps(err),400

'''
 the web routes
'''
# --------------------------------

@app.route("/",methods=["GET"])
def index():
	return render_template("index.html")

@app.route("/employes",methods=["GET"])
def show():
	return render_template("employes.html")

@app.route("/ajouter_employe",methods=["GET"])
def create():
	return render_template("ajouter_employe.html")

@app.route("/modifer_employe",methods=["GET"])
def update():
	return render_template("modifier_employe.html")


'''
 the api routes
'''
# --------------------------------

@app.route("/api/auth",methods=["POST"])
def auth_api():
	common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
	try:
		uid = common.authenticate(db,request.json["username"],request.json["password"],{})
		return str(uid)
	except:
		return "Erreur lors de l'authentification des employes.\n",400


@app.route("/api/employes",methods=['GET',"POST"])
def employes_api():
	return call(["hr.employee","search_read",[[]]],"Erreur lors de l'affichage des employes\n")


@app.route("/api/employe/<int:_id>",methods=['GET','POST'])
def employe_api(_id):
	return call(["hr.employee","read",[[_id]]],"Erreur lors de l'affichage de l'employes\n")


@app.route("/api/employe/cancel/<int:_id>",methods=['GET','POST'])
def cancel_api(_id):
	return call(["hr.employee","write",[[_id],{"state":"cancel"}]],"Erreur lors de l'annulation de l'employe.\n")

@app.route("/api/employe/delete/<int:_id>",methods=['GET','POST'])
def delete_api(_id):
	return call(["hr.employee","unlink",[[_id]]],"Erreur lors de la suppresion de l'employe.\n")

@app.route("/api/employe/update/<int:_id>",methods=['GET','POST'])
def update_api(_id):
	return call(["hr.employee","write",[[_id],{"name":request.json['name'],"work_email":request.json['email']}]],"Erreur lors de la creation de l'employe.\n")

@app.route("/api/employe/create",methods=['GET','POST'])
def create_api():
	return call(["hr.employee","create",[{"name":request.json['name'],"work_email":request.json['email']}]],"Erreur lors de la creation de l'employe.\n")

if __name__ == "__main__":
	app.run(host='0.0.0.0')
