from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin
import requests as r

import sys

app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

def check_username(website, username):
	url = {
	'pinterest' :'https://in.{}.com/{}/'.format(website, username),
	'gitlab'    :'https://{}.com/{}/'.format(website, username),
	'tumblr'    :'https://{}.{}.com'.format(username, website),
	'behance'   :'https://{}.net/{}'.format(website, username)
	}.get(website, 'https://{}.com/{}'.format(website, username)) # default

	if website in ['pinterest', 'gitlab']:
		res  = r.get(url)
		code = 200 if bytes(username, encoding='utf-8') in res.content \
			else 404

		return {'status': code, 'url': url}
	
	else:
		return {'status': r.get(url).status_code, 'url': url}

# API endpoints
@app.route('/')
@cross_origin(origin='*')
def hello():
	return "Hello world! The app seems to be working!"

@app.route('/check/<website>/<username>', methods=['GET'])
@cross_origin(origin='*')
def check(website, username):
	return jsonify(check_username(website, username))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8521)