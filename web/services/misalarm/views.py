from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from misalarm.models import MisAlarmCommand
from misalarm.models import NewBusiness
from datetime import datetime
import json

@csrf_exempt
def commands(request):
    status_code = 200
    if request.method == 'POST':
        if 'commands' in request.POST:
            cmds = json.loads(request.POST['commands'])
            [MisAlarmCommand.objects.create(command=cmd) for cmd in cmds]
            contents = {
                'msg': 'commands record created!',
                'code': 201
            }
            status_code = 201
        else:
            contents = {
                'msg': 'argument commands missing!',
                'code': 400
            }
            status_code = 400
    elif request.method == 'GET':
        if 'timestamp' in request.GET:
            timestamp = float(request.GET['timestamp'])
            prev_time = datetime.fromtimestamp(timestamp)
            new_commands = MisAlarmCommand.objects.filter(time__gt=prev_time)
            contents = [obj.command for obj in new_commands]

        else:
            contents = {
                'msg': 'argument timestamp missed!',
                'code': 400
            }
            status_code = 400

    else:
        # unsupported method
        contents = {
            'msg': 'unsupport request method, only get and post legal!',
            'code': 420
        }
        status_code = 405

    return HttpResponse(json.dumps(contents, ensure_ascii=False), content_type="application/json,charset=utf-8",
                        status=status_code)
@csrf_exempt
def new_business_ip(request):
    status_code = 200
    msg = ''
    code = 200
    data = None
    if request.method == 'POST':
        if 'addresses' in request.POST:
            addrs = json.loads(request.POST['addresses'])
            new_ips = [NewBusiness(ip_addr=addr) for addr in addrs]
            NewBusiness.objects.bulk_create(new_ips)
            status_code = 201
            msg = 'new ip address created!'
            code = 201

        else:
            status_code = 400
            msg = 'missing addresses parameter!'
            code = 400
    elif request.method == 'GET':
        data = [obj.ip_addr for obj in NewBusiness.objects.all()]

        status_code = 200
        msg = 'get ip addr successfully'
        code = 200
    else:
        msg = 'unsupport method!'
        code  = 405
        status_code = 405
    contents = {
        'msg': msg,
        'code': code,
        'data': data
    }
    return HttpResponse(json.dumps(contents, ensure_ascii=False), content_type="application/json,charset=utf-8",
                        status=status_code)