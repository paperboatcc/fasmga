from flask import Flask, render_template, request, redirect, send_from_directory
from replit import db
import random, string, json, os, validators



url = "https://fasm.ga/"
siteName = "Fasm.ga"
anonymousUser = "anonymous"



users = json.loads(os.getenv("IDS"))

app = Flask('app')

def siteLog(path, type, returned, htmlCode):
	path = checkLogLength("| Path: {}".format(path))
	type = checkLogLength("| Type: {}".format(type))
	returned = checkLogLength("| Returned: {}".format(returned))
	print("+-------------------------------------------------------------------------------------------+")
	print("| API Request                                                                               |")
	print(path + "|")
	print(type + "|")
	print(returned + "|")
	print("| HTML Code: {}                                                                            |".format(str(htmlCode)))
	print("+-------------------------------------------------------------------------------------------+")

def checkLogLength(x):
	while len(x) < 92:
		x = x + " "
	return x

def newString():
	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(8))
	return result_str

def getStrings(id):
	urls = db["user_id_" + id]
	return urls

def compileLine(id): # When passed the id for a short URL, returns a preformatted html table line
	return '<tr><td>' + id[10:] + '</td><td>' + db[id] + '</td><td>' + '<a href ="https://fasm.ga/delete/' + id[10:] + '">Elimina</a></td><td><a href ="https://fasm.ga/edit/' + id[10:] + '">Modifica</a></td></tr>'

@app.route('/')
def index():
  
	global siteName
	global users
	if not request.headers['X-Replit-User-Id']:
		siteLog("/", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)
	if len(request.headers['X-Replit-User-Id']) != 0:
		siteLog("/", "File", "templates/submit.html", 200)
		return render_template(
		'submit.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		error=""
	)
	else:
		siteLog("/", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)

@app.route('/custom')
def custom():
	global siteName
	global users
	if not request.headers['X-Replit-User-Id']:
		siteLog("/custom", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)
	if len(request.headers['X-Replit-User-Id']) != 0:
		siteLog("/custom", "File", "templates/custom.html", 200)
		return render_template(
		'custom.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		error=""
	)
	else:
		siteLog("/custom", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)


@app.route('/wp-login.php')
def wploginphp():
	global siteName
	siteLog("/wp-login.php", "Redirect", "/dash", 302)
	return redirect(url + 'dash')

@app.route('/dash')
def dashboard():
    idTable = ""
    global siteName
    try:
        ids = getStrings(request.headers['X-Replit-User-Id'])
        for id in ids:
            idTable = idTable + compileLine(id)
            siteLog("/dash", "File", "templates/dashboard.html", 200)
            return render_template('dashboard.html',siteName=siteName, user_id=request.headers['X-Replit-User-Id'],user_name=request.headers['X-Replit-User-Name'],
            user_roles=request.headers['X-Replit-User-Roles'],idTable = idTable,error = "")
    except:
        siteLog("/dash", "File", "templates/dashboard.html", 200)
        return render_template(
			'dashboard.html',
			siteName=siteName,
			user_id=request.headers['X-Replit-User-Id'],
			user_name=request.headers['X-Replit-User-Name'],
			user_roles=request.headers['X-Replit-User-Roles'],
			idTable = idTable,
			error = "<center><h6>Non hai ancora creato un URL.</h6></center>"
		)

@app.route('/delete/<string:id>')
def delete(id):
	global siteName
	if not id:
		id = "Please stop trying to break the site lol"
	siteLog("/delete/" + str(id), "File", "templates/delete.html", 200)
	return render_template(
		'delete.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles'],
		id = id
	)

@app.route('/delete/')
def nodeleteurl():
	global siteName
	siteLog("/delete/" + str(id), "File", "templates/delete.html", 200)
	return render_template('error.html', siteName=siteName, code = "400", message = "Non hai inserito un URL da eliminare.")

@app.route('/delete')
def nodeleteurl2():
	global siteName
	siteLog("/delete/" + str(id), "File", "templates/delete.html", 200)
	return render_template('error.html', siteName=siteName, code = "400", message = "Non hai inserito un URL da eliminare.")

@app.route('/edit/')
def noediturl():
	global siteName
	siteLog("/edit/" + str(id), "File", "templates/edit.html", 200)
	return render_template('error.html', siteName=siteName, code = "400", message = "Non hai inserito un URL da modificare.")

@app.route('/edit')
def noediturl2():
	global siteName
	siteLog("/edit/" + str(id), "File", "templates/edit.html", 200)
	return render_template('error.html', siteName=siteName, code = "400", message = "Non hai inserito un URL da modificare.")

@app.route('/edit/<string:id>')
def edit(id):
	global siteName
	siteLog("/edit/" + str(id), "File", "templates/edit.html", 200)
	return render_template(
		'edit.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles'],
		oldurl = db["short_url_" + id],
		id = id
	)

@app.route('/del', methods=['POST'])
def deleteEntry():
	global siteName
	if len(request.headers['X-Replit-User-Id']) != 0:
		user_id = request.headers['X-Replit-User-Id']
		id = request.form['id']
		users_ids = db["user_id_" + user_id]
		try:
			users_ids.remove("short_url_" + id)
			del db["short_url_" + id]
			db["user_id_" + user_id] = users_ids
			siteLog("/del", "Redirect", "/dash", 302)
			return redirect(url + "dash", 302)
		except:
			siteLog("/del", "File", "templates/error.html", 401)
			return render_template('error.html', code = "401", siteName=siteName, message = "Non sei il proprietario di questo URL.")

@app.route('/edt', methods=['POST'])
def editEntry():
	global siteName
	global url
	if len(request.headers['X-Replit-User-Id']) != 0:
		user_id = request.headers['X-Replit-User-Id']
		id = request.form['id']
		newurl = request.form['newurl']
		try:
			db["short_url_" + id] = newurl
			siteLog("/del", "Redirect", "/dash", 302)
			return redirect(url + "dash", 302)
		except:
			siteLog("/edt", "File", "templates/error.html", 401)
			return render_template('error.html', code = "401", siteName=siteName, message = "Non sei il proprietario di questo URL.")

@app.route('/favicon.ico')
def favicon():
	siteLog("/favicon.ico", "File", "static/favicon.ico", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/.css')
def css():
	siteLog("/.css", "File", "static/styles.css", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'styles.css')

@app.route('/sitemap.xml')
def sitemap():
	siteLog("/sitemap.xml", "File", "static/sitemap.xml", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/robots.txt')
def robots():
	siteLog("/robots.txt", "File", "static/robots.txt", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/<string:key>', methods=['GET'])
def sendUrl(key):
    try:
        global siteName
        key = "short_url_" + key
        redirectUrl = db[key]
        siteLog("/" + str(key), "Redirect", redirectUrl, 302)
        return redirect(redirectUrl, 302)
    except:
        siteLog("/" + str(key), "File", "templates/error.html", 404)
        return render_template('error.html', code = "404", siteName=siteName, message = "URL non esistente")

@app.route('/<string:key>/', methods=['GET'])
def sendUrl2(key):
    try:
        global siteName
        key = "short_url_" + key
        redirectUrl = db[key]
        siteLog("/" + str(key), "Redirect", redirectUrl, 302)
        return redirect(redirectUrl, 302)
    except:
        siteLog("/" + str(key), "File", "templates/error.html", 404)
        return render_template('error.html', code = "404", siteName=siteName, message = "URL non esistente")

@app.route('/get/<string:id>')
def get(id):
  global siteName
  siteLog("/get/" + str(id), "File", "templates/geturl.html", 200)
  try:
	  return render_template(
		  'geturl.html',
	  	siteName=siteName,
	  	oldurl = db["short_url_" + id],
	  	id = id[16:]
  	)
  except:
    return render_template('error.html', code = "404", siteName=siteName, message = "URL non esistente")

@app.route('/get')
def getpage():
	global siteName
	siteLog("/get/" + str(id), "File", "templates/get.html", 200)
	return render_template(
		'get.html',
		siteName=siteName
	)

@app.route('/new', methods=['POST'])
def newEntry():
	global siteName
	if len(request.headers['X-Replit-User-Id']) != 0:
		key = "short_url_" + newString()
		keys = list(db.keys())
		while key in keys:
			key = "short_url_" + newString()
			keys = list(db.keys())
		if not validators.url(str(request.form['url'])):
			siteLog("/new", "File", "templates/submit.html", 400)
			return render_template(
				'submit.html',
				siteName=siteName,
				user_id=user,
				user_name=request.headers['X-Replit-User-Name'],
				error="That was not a valid URL. Please enter a valid URL and try again."
			)
		db[key] = request.form['url']
		try:
			strings = list(getStrings(request.headers['X-Replit-User-Id']))
		except:
			strings = []
		strings.append(key)
		db["user_id_" + request.headers['X-Replit-User-Id']] = strings
		siteLog("/new", "File", "templates/done.html", 200)
		return render_template('done.html', siteName=siteName, newUrl = url + key[10:])

@app.route('/newl', methods=['POST'])
def newWithoutLogin():
        global siteName
        key = "short_url_" + newString()
        keys = list(db.keys())
        while key in keys:
            key = "short_url_" + newString()
            keys = list(db.keys())
        if not validators.url(str(request.form['url'])):
            siteLog("/newl", "File", "templates/index.html", 400)
            return render_template(
                'index.html',
                siteName=siteName,
                user_id=1000000,
                user_name=anonymousUser,
                error="That was not a valid URL. Please enter a valid URL and try again."
            )
        db[key] = request.form['url']
        try:
            strings = []
        except:
            strings = []
        strings.append(key)
        db["user_id_1000000"] = strings
        siteLog("/newl", "File", "templates/done.html", 200)
        return render_template('done.html', siteName=siteName, newUrl = url + key[10:])

@app.route('/newcustom', methods=['POST'])
def newCustom():
	global siteName
	if len(request.headers['X-Replit-User-Id']) != 0:
		key = "short_url_" + request.form['id']
		keys = list(db.keys())
		if key in keys:
			return render_template('error.html', siteName=siteName, code = "401", message = "ID già esistente.")
		if not validators.url(str(request.form['url'])):
			siteLog("/new", "File", "templates/manual.html", 400)
			return render_template(
				'manual.html',
				siteName=siteName,
				user_id=user,
				user_name=request.headers['X-Replit-User-Name'],
				error="That was not a valid URL. Please enter a valid URL and try again."
			)
		db[key] = request.form['url']
		try:
			strings = list(getStrings(request.headers['X-Replit-User-Id']))
		except:
			strings = []
		strings.append(key)
		db["user_id_" + request.headers['X-Replit-User-Id']] = strings
		siteLog("/newcustom", "File", "templates/done.html", 200)
		return render_template('done.html', siteName=siteName, newUrl = url + key[10:])

@app.route("/placeholder")
def placeholder():
  return "<!DOCTYPE html><html><body><code>Never gonna give you up<br>Never gonna let you down<br>Never gonna run around and desert you<br>Never gonna make you cry<br>Never gonna say goodbye<br>Never gonna tell a lie and hurt you</code></body></html>"

@app.route("/placeholder")
def placeholder2():
  return "<!DOCTYPE html><html><body><code>Never gonna give you up<br>Never gonna let you down<br>Never gonna run around and desert you<br>Never gonna make you cry<br>Never gonna say goodbye<br>Never gonna tell a lie and hurt you</code></body></html>"

@app.route("/premium")
def premium():
  return "<code>Fasm.ga è 100% gratuito e sarà sempre così.</code>"

@app.route("/premium")
def premium2():
  return "<code>Fasm.ga è 100% gratuito e sarà sempre così.</code>"

@app.route("/☭")
def ee(): # Easter Egg di th3atom
  return redirect("https://www.youtube.com/watch?v=knzDT7-7HEg", 302)

@app.route("/☭/")
def eee(): # Easter Egg di th3atom
  return redirect("https://www.youtube.com/watch?v=knzDT7-7HEg", 302)

@app.errorhandler(400)
def error_bad_request(e):
	global siteName
	siteLog("Bad Request", "Error", "templates/error.html", 400)
	return render_template('error.html', siteName=siteName, code = "400", message = "Richiesta formulata in modo errato.")

@app.errorhandler(401)
def error_unauthorized(e):
	global siteName
	siteLog("Unauthorized", "Error", "templates/error.html", 401)
	return render_template('error.html', siteName=siteName, code = "401", message = "Non autorizzato.")

@app.errorhandler(403)
def error_forbidden(e):
	global siteName
	siteLog("Forbidden", "Error", "templates/error.html", 403)
	return render_template('error.html', siteName=siteName, code = "403", message = "Accesso vietato.")

@app.errorhandler(404)
def error_page_not_found(e):
	global siteName
	siteLog("Page not Found", "Error", "templates/error.html", 404)
	return render_template('error.html', siteName=siteName, code = "404", message = "Pagina non trovata.")

@app.errorhandler(409)
def error_conflict(e):
	global siteName
	siteLog("Conflict", "Error", "templates/error.html", 409)
	return render_template('error.html', siteName=siteName, code = "409", message = "Conflitto.")

@app.errorhandler(501)
def error_internal_server_error(e):
	global siteName
	siteLog("Internal Server Error", "Error", "templates/error.html", 501)
	return render_template('error.html', siteName=siteName, code = "500", message = "Errore del sito.")

@app.errorhandler(501)
def error_not_implemented(e):
	global siteName
	siteLog("Not Implemented", "Error", "templates/error.html", 501)
	return render_template('error.html', siteName=siteName, code = "501", message = "Not Implemented")

@app.errorhandler(502)
def error_bad_gateway(e):
	global siteName
	siteLog("Bad Gateway", "Error", "templates/error.html", 502)
	return render_template('error.html', siteName=siteName, code = "502", message = "")

app.run(host='0.0.0.0', port=8080)