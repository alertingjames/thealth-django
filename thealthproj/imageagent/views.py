import requests
from django.core.mail import EmailMultiAlternatives

from django.core.files.storage import FileSystemStorage
import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import time
from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from random import randint
from pyfcm import FCMNotification
import pyrebase


from thealth.models import IMember
from thealth.serializers import IMemberSerializer


def index(request):
    return HttpResponse('<h1>Hello, I am ImageAgent!</h1>')

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def signup(request):

    if request.method == 'POST':

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        users = IMember.objects.filter(email=email)
        count = users.count()
        if count == 0:
            member = IMember()
            member.name = name
            member.email = email
            member.password = password
            member.registered_time = str(int(round(time.time() * 1000)))
            member.save()

            serializer = IMemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            users = IMember.objects.filter(email=email, password=password)
            count = users.count()
            if count == 0:
                resp_er = {'result_code': '1'}
                return HttpResponse(json.dumps(resp_er))
            else:
                resp_er = {'result_code': '2'}
                return HttpResponse(json.dumps(resp_er))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if password != '':
            members = IMember.objects.filter(email=email, password=password)
        else:
            members = IMember.objects.filter(email=email)
        resp = {}
        if members.count() > 0:
            member = members[0]
            serializer = IMemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            members = IMember.objects.filter(email=email)
            if members.count() > 0:
                resp = {'result_code': '2'}
            else: resp = {'result_code':'1'}

        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        members = IMember.objects.filter(email=email)
        if members.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        member = members[0]

        message = 'You are allowed to reset your password from your request.<br><br><a href="https://www.thealth.app/imageagent/resetpassword?uid=' + str(member.pk) + '">please click this link to reset your password</a>'

        html =  """\
                    <html>
                        <head></head>
                        <body>
                            <a href="#"><img src="https://www.thealth.app/static/images/icon.png" style="width:120px;height:120px;border-radius: 5%; margin-left:25px;"/></a>
                            <h2 style="margin-left:10px; color:#02839a;">ImageAgent Member's Security Update Information</h2>
                            <div style="font-size:14px; word-wrap: break-word;">
                                {mes}
                            </div>
                        </body>
                    </html>
                """
        html = html.format(mes=message)

        fromEmail = settings.IMAGEAGENT_ADMIN_EMAIL
        toEmailList = []
        toEmailList.append(email)
        msg = EmailMultiAlternatives('We allowed you to reset your password', '', fromEmail, toEmailList)
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)

        return HttpResponse(json.dumps({'result_code': '0'}))



def resetpassword(request):
    member_id = request.GET['uid']
    member = IMember.objects.get(id=int(member_id))
    return render(request, 'imageagent/resetpwd.html', {'member':member})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def rstpwd(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        if password != repassword:
            return render(request, 'imageagent/result.html',
                          {'response': 'Please enter the same password.'})
        members = IMember.objects.filter(id=int(member_id))
        if members.count() > 0:
            member = members[0]
            member.password = password
            member.save()
            return render(request, 'imageagent/result.html',
                          {'response': 'Password has been reset successfully.'})
        else:
            return render(request, 'imageagent/result.html',
                          {'response': 'You haven\'t been registered.'})























































