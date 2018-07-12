from django.shortcuts import render
import paramiko
import spur
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import user
# Create your views here.

@csrf_exempt
def home (request) :
	if request.method == 'GET':
		if 'email' in request.session:
			return render(request, 'cmd.html', {})
		else:
			return render(request, 'home.html', {})

	if request.method == 'POST':
		print(request.POST)
		form = request.POST
		if 'email' in form :
			print(form['email'])
			context = { "message":"" }
			try :
				save  = user.objects.get(email=form['email'])
			except :
				context["message"] = "Email doesn't exist"
				return render(request, 'home.html', context)

			if form['password'] == save.password :
				request.session['email'] = save.email
				read_data = ""
				with open('main/lastcmd.txt', 'r') as f:
					read_data = f.read()
				dat = read_data.split(" ")
				try:
					context = {"ip":dat[0], "usernm":dat[1], "pass":dat[2]}
				except Exception as e :
					context= {}
				print(context)
				return render (request, "cmd.html", context)
			context["message"] = "Incorrect  Password"
			return render(request, 'home.html', context)
		else:
			try:
				del request.session['email']
			except:
				pass
			return render(request, 'home.html', {})






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

@csrf_exempt
def runcmd (request) :
	try :
		data = request.POST
		print (data)
		with open('main/lastcmd.txt', 'w') as f:
			f.write(data["ip"]+" " +data["user"]+" " +data["pass"])
		cmd = data['cmd']
		shell = spur.SshShell(hostname=data['ip'], username=data['user'], password=data['pass'],missing_host_key=spur.ssh.MissingHostKey.accept)
		result = shell.run(cmd.split(" "))
		print (result.output.decode("utf-8").replace("↵","\n")) 
		return JsonResponse({"output":result.output.decode("utf-8").replace("↵","\n")})
	except Exception as e :
		return JsonResponse({"output":str(e)})