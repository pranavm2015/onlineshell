from django.shortcuts import render
import paramiko
import spur
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import user
import datetime
# Create your views here.

@csrf_exempt
def home (request) :
	if request.method == 'GET':
		if 'email' in request.session:
			try :
				save  = user.objects.get(email=form['email'])
			except :
				return render(request, 'home.html', {})

			if request.session['password'] == save.password :
				request.session['email'] = save.email
				request.session['password'] = save.password
				ip = request.COOKIES.get('ip','')
				username = request.COOKIES.get('username','')
				password = request.COOKIES.get('pass','')
				context={'ip':ip,'user':username,'pass':password}
				print(1)
				return render (request, "cmd.html", context)
			return render(request, 'home.html', {})

		else:
			print(2)
			return render(request, 'home.html', {})

	if request.method == 'POST':
		form = request.POST
		if 'email' in form :
			context = { "message":"" }
			try :
				save  = user.objects.get(email=form['email'])
			except :
				context["message"] = "Email doesn't exist"
				return render(request, 'home.html', context)

			if form['password'] == save.password :
				request.session['email'] = save.email
				request.session['password'] = save.password
				ip = request.COOKIES.get('ip','')
				username = request.COOKIES.get('username','')
				password = request.COOKIES.get('pass','')
				context={'ip':ip,'usernm':username,'pass':password}
				print(context)
				return render (request, "cmd.html", context)
			context["message"] = "Incorrect  Password"
			return render(request, 'home.html', context)
		else:
			try:
				del request.session['email']
			except:
				pass

			response =  render(request, 'home.html', {})
			response.delete_cookie('ip')
			response.delete_cookie('username')
			response.delete_cookie('pass')
			return response

@csrf_exempt
def runcmd (request) :

	max_age = 3*24*60*60 # 3 days
	expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
	
	try :
		data = request.POST
		print ("enter")
		cmd = data['cmd']
		shell = spur.SshShell(hostname=data['ip'], username=data['user'], password=data['pass'],missing_host_key=spur.ssh.MissingHostKey.accept)
		result = shell.run(cmd.split(" "))
		print (result.output.decode("utf-8").replace("↵","\n")) 
		response =  JsonResponse({"output":result.output.decode("utf-8").replace("↵","\n")})
		response.set_cookie('ip', data['ip'], max_age=max_age, expires=expires)
		response.set_cookie('username', data['user'], max_age=max_age, expires=expires)
		response.set_cookie('pass', data['pass'], max_age=max_age, expires=expires)
		print ("1"+response)
		return response

	except Exception as e :
		response = JsonResponse({"output":str(e)})
		response.set_cookie('ip', data['ip'], max_age=max_age, expires=expires)
		response.set_cookie('username', data['user'], max_age=max_age, expires=expires)
		response.set_cookie('pass', data['pass'], max_age=max_age, expires=expires)
		return response



	# if 'email' in request.session:
	# 	if request.method == 'POST' :
	# 		try:
	# 			del request.session['email']
	# 		except:
	# 			pass
	# 		return render(request, 'home.html', {})
			    
	# 	return render(request, 'cmd.html', {})
	
	# else:
	# 	if request.method == 'POST':
	# 		print(request.POST)
	# 		form = request.POST
	# 		if 'email' in form :
	# 			print(form['email'])
	# 			context = { "message":"" }
	# 			try :
	# 				save  = user.objects.get(email=form['email'])
	# 			except :
	# 				context["message"] = "Email doesn't exist"
	# 				return render(request, 'home.html', context)

	# 			if form['password'] == save.password :
	# 				request.session['email'] = save.email
	# 				read_data = ""
	# 				with open('main/lastcmd.txt', 'r') as f:
	# 					read_data = f.read()
	# 				dat = read_data.split(" ")
	# 				try:
	# 					context = {"ip":dat[0], "usernm":dat[1], "pass":dat[2]}
	# 				except Exception as e :
	# 					context= {}
	# 				print(context)
	# 				return render (request, "dash.html", context)
	# 			context["message"] = "Incorrect  Password"
	# 			return render(request, 'home.html', context)

	# 	if request.method == 'GET':
	# 		return render(request, 'home.html', {})


# @csrf_exempt
# def cmdline (request) :
# 	read_data = ""
# 	with open('main/lastcmd.txt', 'r') as f:
# 		read_data = f.read()
# 	dat = read_data.split(" ")
# 	try:
# 		context = {"ip":dat[0], "usernm":dat[1], "pass":dat[2]}
# 	except Exception as e :
# 		context= {}
# 	print(context)
# 	return render (request, "home.html", context)
