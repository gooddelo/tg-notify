from flask import Flask,Response,redirect,request,abort
import bot
import requests,json
from flask_cors import CORS, cross_origin
import os

GCAPTCHA = os.environ['GCAPTCHA']


def start():

	app = Flask(__name__)
	CORS(app)
	
	@app.route('/', methods=['GET'])
	def index():
		return "<h1>Gooddelo API</h1><p>by Tojefin</p>", 200

	@app.errorhandler(404)
	def page_not_found(e):
		return "<h1>404</h1><p>The resource could not be found.</p>", 404

	@app.route('/api/v1/sendform/', methods=['POST'])
	@cross_origin(origin='*')
	def api():
		info = ""
		
		name = request.form.get('Name')
		if name:
			info = info + f"\n 👨: {name}"
		phone = request.form.get('Phone')
		if phone:
			info = info + f"\n 📞: {phone}"
		email = request.form.get('Email')
		if email:
			info = info + f"\n 📧: {email}"
		comment = request.form.get('Comment')
		if comment:
			info = info + f"\n 📄: {comment}"
		token = request.form.get('token')
		VerifyCAPTCHA(token)
		
		bot.Send(
				f"{request.referrer}\n Получена заявка{info}"
		)

		if request.form.get('getStatus'):
			return Response("{'done': true}", status=200, mimetype='application/json')
		
		return redirect(request.referrer)

	app.run(host='0.0.0.0', port=80)

def VerifyCAPTCHA(token):
	res = requests.get(f'https://www.google.com/recaptcha/api/siteverify?secret={GCAPTCHA}&response={token}')
	data = json.loads(res.text)
	if data['success'] != True:
		return abort(401)
	