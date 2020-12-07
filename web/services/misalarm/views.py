from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from misalarm.models import MisAlarmCommand
from misalarm.models import NewBusiness
from datetime import datetime
import json

@csrf_exempt
def commands(request):
    status_code = 200
    data = None
    if request.method == 'POST':
        if 'commands' in request.POST:
            cmds = json.loads(request.POST['commands'])
            new_commands = [MisAlarmCommand(command=cmd) for cmd in cmds]
            try:
                MisAlarmCommand.objects.bulk_create(new_commands)
            except Exception as e:
                print(e)
                pass
            msg = 'commands record created!'
            code = 201
            status_code = 201
        else:
            msg = 'argument commands missing!'
            code = 400
            status_code = 400
    elif request.method == 'GET':
        if 'timestamp' in request.GET:
            timestamp = float(request.GET['timestamp'])
            prev_time = datetime.fromtimestamp(timestamp)
            new_commands = MisAlarmCommand.objects.filter(time__gt=prev_time)
            data = [obj.command for obj in new_commands]
            msg = 'get commands newer than {}!'.format(prev_time.ctime())
            code = 200
        else:
            new_commands = MisAlarmCommand.objects.all()
            data = [obj.command for obj in new_commands]
            msg = 'get all commands'
            code = 200
            status_code = 200
    elif request.method == 'DELETE':
        params=QueryDict(request.body)
        commands = params.get('commands', default=[])
        if commands:
            MisAlarmCommand.objects.filter(command__in=commands).delete()
            msg = 'commands deleted!'
        msg = 'missing commands parameter!'
        code = 200
        status_code = 200
    else:
        # unsupported method
        msg = 'unsupport request method, only get and post legal!'
        code = 405

        status_code = 405
    contents = {
        'msg': msg,
        'code': code,
        'data': data
    }
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
            try:
                NewBusiness.objects.bulk_create(new_ips)
            except Exception as e:
                print(e)
                pass
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
    elif request.method == 'DELETE':
        params = QueryDict(request.body)
        addrs = json.loads(params.get('addresses'))
        if addrs:
            NewBusiness.objects.filter(ip_addr__in=addrs).delete()
            msg = 'ip addresses deleted sucessfully!'
        code = 200
        status_code = 200
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