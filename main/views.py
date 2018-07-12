from django.shortcuts import render
import paramiko
import spur
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

@csrf_exempt
def home (request) :
	read_data = ""
	with open('main/lastcmd.txt', 'r') as f:
		read_data = f.read()
	dat = read_data.split(" ")
	try:
		context = {"ip":dat[0], "usernm":dat[1], "pass":dat[2]}
	except Exception as e :
		context= {}
	print(context)
	return render (request, "home.html", context)

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