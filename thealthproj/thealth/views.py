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

from thealth.models import Member, Code, Feed, FeedPicture, FeedComment, FeedLike, FeedSave, FeedFollow
from thealth.serializers import MemberSerializer, FeedSerializer, FeedPictureSerializer, FeedCommentSerializer


config = {
    "apiKey": "AIzaSyAKqMHFeyjqlDQBEPPQZG5TQVIyE764L_w",
    "authDomain": "thealth-a9c9d.firebaseapp.com",
    "databaseURL": "https://thealth-a9c9d.firebaseio.com",
    "storageBucket": "thealth-a9c9d.appspot.com"
}

firebase = pyrebase.initialize_app(config)


def index(request):
    return HttpResponse('<h2>Hello I am THEALTH backend!</h2>')


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def signup(request):

    if request.method == 'POST':

        eml = request.POST.get('email', '')
        password = request.POST.get('password', '')
        picture_url = request.POST.get('picture_url', '')

        users = Member.objects.filter(email=eml)
        count = users.count()
        if count == 0:
            member = Member()
            member.email = eml
            if picture_url != '': member.picture_url = picture_url
            else: member.picture_url = settings.URL + '/static/images/user.png'
            member.password = password
            member.auth_status = str(random_with_N_digits(5))
            member.registered_time = str(int(round(time.time() * 1000)))
            member.latitude = '0'
            member.longitude = '0'
            member.followers = '0'
            member.followings = '0'
            member.posts = '0'
            member.save()

            if password != '': sendcode(member.email, member.auth_status)
            else:
                member.auth_status = 'verified'
                member.save()

            serializer = MemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            users = Member.objects.filter(email=eml, password=password)
            count = users.count()
            if count == 0:
                resp_er = {'result_code': '1'}
                return HttpResponse(json.dumps(resp_er))
            else:
                resp_er = {'result_code': '2'}
                return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



def sendcode(email, code):

    message = 'You signed up with our Thealth app. We want to verify your email by a verification code.<br>Your verification code: ' + code + '<br>Please enter this verification code in your app to validate your email.<br><br>Thealth'

    html =  """\
                <html>
                    <head></head>
                    <body>
                        <a href="#"><img src="https://www.thealth.app/static/images/logo.png" style="width:120px;height:120px;border-radius: 8%; margin-left:25px;"/></a>
                        <h3 style="margin-left:10px; color:#02839a;">Thealth User Authentication</h3>
                        <div style="font-size:12px; word-break: break-all; word-wrap: break-word;">
                            {mes}
                        </div>
                    </body>
                </html>
            """
    html = html.format(mes=message)

    fromEmail = settings.ADMIN_EMAIL
    toEmailList = []
    toEmailList.append(email)
    msg = EmailMultiAlternatives('THEALTH OPT Authentication', '', fromEmail, toEmailList)
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def codesubmit(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '')
        code = request.POST.get('code', '')

        resp = {'result_code':'2'}
        users = Member.objects.filter(id=member_id)
        count = users.count()
        if count > 0:
            member = users[0]
            if member.auth_status != 'verified' and member.auth_status == code:
                member.auth_status = 'verified'
                member.save()
                resp = {'result_code':'0'}
            else:
                resp = {'result_code':'1'}

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def resendcode(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '')
        resp = {'result_code':'1'}
        users = Member.objects.filter(id=member_id)
        count = users.count()
        if count > 0:
            member = users[0]
            member.auth_status = str(random_with_N_digits(5))
            member.save()

            sendcode(member.email, member.auth_status)

            resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))




@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if password != '':
            members = Member.objects.filter(email=email, password=password)
        else:
            members = Member.objects.filter(email=email)
        resp = {}
        if members.count() > 0:
            member = members[0]
            if member.auth_status != 'verified':
                member.auth_status = str(random_with_N_digits(5))
                member.save()
                if password != '': sendcode(member.email, member.auth_status)
            serializer = MemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            members = Member.objects.filter(email=email)
            if members.count() > 0:
                member = members[0]
                if member.password == '':
                    if member.auth_status != 'verified':
                        member.auth_status = str(random_with_N_digits(5))
                        member.save()
                        if password != '': sendcode(member.email, member.auth_status)
                    serializer = MemberSerializer(member, many=False)
                    resp = {'result_code': '0', 'data':serializer.data}
                    return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
                else:
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

        usrs = Member.objects.filter(email=email)
        if usrs.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        member = usrs[0]
        cd = Code()
        cd.member_id = member.pk
        cd.code = str(random_with_N_digits(5))
        cd.save()

        codesendtoemail(email, cd.code)

        return HttpResponse(json.dumps({'result_code': '0'}))


def codesendtoemail(email, code):
    message = 'You are allowed to reset your password from your request.<br>For it, we want to verify your email by a verification code.<br>Your verification code: ' + code + '<br>Please enter this verification code in your app to validate your email.<br><br>Thealth'

    html =  """\
            <html>
                <head></head>
                <body>
                    <a href="#"><img src="https://www.thealth.app/static/images/logo.png" style="width:120px;height:120px;border-radius: 8%; margin-left:25px;"/></a>
                    <h3 style="margin-left:10px; color:#02839a;">Thealth User Authentication</h3>
                    <div style="font-size:12px; word-break: break-all; word-wrap: break-word;">
                        {mes}
                    </div>
                </body>
            </html>
        """
    html = html.format(mes=message)

    fromEmail = settings.ADMIN_EMAIL
    toEmailList = []
    toEmailList.append(email)
    msg = EmailMultiAlternatives('THEALTH OPT Authentication', '', fromEmail, toEmailList)
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def vcoderesend(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        usrs = Member.objects.filter(email=email)
        if usrs.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        member = usrs[0]
        cds = Code.objects.filter(member_id=member.pk)
        cd = cds[0]
        cd.code = str(random_with_N_digits(5))
        cd.save()

        codesendtoemail(email, cd.code)

        return HttpResponse(json.dumps({'result_code': '0'}))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def sendvcode(request):

    if request.method == 'POST':

        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        resp = {'result_code':'2'}
        usrs = Member.objects.filter(email=email)
        if usrs.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))
        member = usrs[0]
        cds = Code.objects.filter(member_id=member.pk)
        cd = cds[0]
        if code == cd.code:
            cd.delete()
            resp = {'result_code':'0'}

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def pwdreset(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        members = Member.objects.filter(email=email)
        if members.count() > 0:
            member = members[0]
            oldPassword = member.password
            member.password = password
            member.save()
            resp = {'result_code':'0', 'old_password':oldPassword}
        else:
            resp = {'result_code':'1'}

        return HttpResponse(json.dumps(resp))




def resetpassword(request):
    email = request.GET['email']
    return render(request, 'thealth/resetpwd.html', {'email':email})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def rstpwd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        if password != repassword:
            return render(request, 'thealth/result.html',
                          {'response': 'Please enter the same password.'})
        members = Member.objects.filter(email=email)
        if members.count() > 0:
            member = members[0]
            member.password = password
            member.save()
            return render(request, 'thealth/result.html',
                          {'response': 'Password has been reset successfully.'})
        else:
            return render(request, 'thealth/result.html',
                          {'response': 'You haven\'t been registered.'})
    else: pass



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def registerProfile(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        latitude = request.POST.get('latitude', '0')
        longitude = request.POST.get('longitude', '0')

        users = Member.objects.filter(id=member_id)
        count = users.count()
        if count > 0:
            member = users[0]
            member.name = name
            member.phone_number = phone_number
            member.address = address
            member.latitude = latitude
            member.longitude = longitude

            member.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    member.picture_url = settings.URL + uploaded_url
                    member.save()

            serializer = MemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def postnewfeed(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        description = request.POST.get('description', '')
        privacy = request.POST.get('privacy', '')
        location = request.POST.get('location', '')
        latitude = request.POST.get('latitude', '0')
        longitude = request.POST.get('longitude', '0')

        feed = Feed()
        feed.member_id = member_id
        feed.description = description
        feed.privacy = privacy
        feed.location = location
        feed.latitude = latitude
        feed.longitude = longitude
        feed.posted_time = str(int(round(time.time() * 1000)))
        feed.likes = '0'
        feed.comments = '0'

        fs = FileSystemStorage()
        try:
            video = request.FILES['video']
            thumb = request.FILES['thumb']

            filename = fs.save(video.name, video)
            uploaded_url = fs.url(filename)
            feed.video_url = settings.URL + uploaded_url
            filename = fs.save(thumb.name, thumb)
            uploaded_url = fs.url(filename)
            feed.picture_url = settings.URL + uploaded_url
        except MultiValueDictKeyError:
            print('no video uploaded')

        feed.save()

        try:
            ps = request.FILES.getlist('pictures')
            i = 0
            for f in ps:
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                p = FeedPicture()
                p.feed_id = feed.pk
                p.member_id = member_id
                p.picture_url = settings.URL + uploaded_url
                p.save()
                if i == 1:
                    feed.picture_url = settings.URL + uploaded_url
                    feed.save()

        except MultiValueDictKeyError:
            print('no picture uploaded')

        # toids = getFollowMemberIDs(member_id)
        # message = member.name + ' posted a new feed.'
        # sendPostMessageToFriends(member_id, toids, message, 'feed', feed.pk)

        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def homefeeds(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        feedList = []
        feeds = Feed.objects.all().order_by('-id')
        feedUserList = []
        for feed in feeds:
            likes = FeedLike.objects.filter(feed_id=feed.pk, member_id=member_id)
            if likes.count() > 0:
                feed.is_liked = 'yes'
            else:feed.is_liked = 'no'
            saves = FeedSave.objects.filter(feed_id=feed.pk, member_id=member_id)
            if saves.count() > 0:
                feed.is_saved = 'yes'
            else:feed.is_saved = 'no'

            pics = FeedPicture.objects.filter(feed_id=feed.pk)
            pic_count = pics.count()

            fmember = Member.objects.get(id=feed.member_id)
            follows = FeedFollow.objects.filter(member_id=fmember.pk, follower_id=member_id)
            if follows.count() > 0:
                if fmember not in feedUserList:
                    feedUserList.append(fmember)

            feedser = FeedSerializer(feed, many=False)
            memberser = MemberSerializer(fmember, many=False)


            data = {
                'feed':feedser.data,
                'member':memberser.data,
                'pic_count': str(pic_count)
            }

            if data not in feedList:
                feedList.append(data)

        membersers = MemberSerializer(feedUserList, many=True)

        resp = {'result_code':'0', 'data':feedList, 'feed_users':membersers.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def likeFeed(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        member_id = request.POST.get('member_id', '1')
        like = FeedLike()
        like.feed_id = feed_id
        like.member_id = member_id
        like.liked_time = str(int(round(time.time() * 1000)))
        like.save()
        feed = Feed.objects.get(id=feed_id)
        feed.likes = str(int(feed.likes) + 1)
        feed.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def unLikeFeed(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        member_id = request.POST.get('member_id', '1')
        likes = FeedLike.objects.filter(feed_id=feed_id, member_id=member_id)
        if likes.count() > 0:
            like = likes[0]
            like.delete()
        feed = Feed.objects.get(id=feed_id)
        feed.likes = str(int(feed.likes) - 1)
        feed.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def saveFeed(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        member_id = request.POST.get('member_id', '1')
        fsave = FeedSave()
        fsave.feed_id = feed_id
        fsave.member_id = member_id
        fsave.saved_time = str(int(round(time.time() * 1000)))
        fsave.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def unSaveFeed(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        member_id = request.POST.get('member_id', '1')
        fsaves = FeedSave.objects.filter(feed_id=feed_id, member_id=member_id)
        if fsaves.count() > 0:
            fsave = fsaves[0]
            fsave.delete()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def feedFollow(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        me_id = request.POST.get('me_id', '1')
        member = Member.objects.get(id=member_id)
        if member is not None:
            follows = FeedFollow.objects.filter(member_id=member.pk, follower_id=me_id)
            if follows.count() == 0:
                follow = FeedFollow()
                follow.member_id = member_id
                follow.follower_id = me_id
                follow.date_time = str(int(round(time.time() * 1000)))
                follow.save()
                member.followers = str(int(member.followers) + 1)
                member.save()
                me = Member.objects.get(id=me_id)
                me.followings = str(int(me.followings) + 1)
                me.save()
            resp = {'result_code':'0'}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def feedUnfollow(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        friend_id = request.POST.get('friend_id', '1')
        friend = Member.objects.get(id=friend_id)
        if friend is not None:
            follows = FeedFollow.objects.filter(member_id=friend_id, follower_id=member_id)
            if follows.count() > 0:
                f = follows[0]
                f.delete()
                friend.followers = str(int(friend.followers) - 1)
                friend.save()
                me = Member.objects.get(id=member_id)
                me.followings = str(int(me.followings) - 1)
                me.save()
            resp = {'result_code':'0'}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getFeedPictures(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        fps = FeedPicture.objects.filter(feed_id=feed_id).order_by('-id')
        serializer = FeedPictureSerializer(fps, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getFeedComments(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        comments = FeedComment.objects.filter(feed_id=feed_id).order_by('-id')
        commentList = []
        for comment in comments:
            member = Member.objects.get(id=comment.member_id)
            commentser = FeedCommentSerializer(comment, many=False)
            memberser = MemberSerializer(member, many=False)
            data = {
                'comment':commentser.data,
                'member':memberser.data
            }
            commentList.append(data)
        resp = {'result_code':'0', 'data':commentList}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def sendFeedComment(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        member_id = request.POST.get('member_id', '1')
        text = request.POST.get('comment', '')
        member = Member.objects.get(id=member_id)
        comment = FeedComment()
        comment.feed_id = feed_id
        comment.member_id = member_id
        comment.comment = text
        comment.commented_time = str(int(round(time.time() * 1000)))
        comment.save()
        feed = Feed.objects.get(id=feed_id)
        feed.comments = str(int(feed.comments) + 1)
        feed.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delFeed(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        feeds = Feed.objects.filter(id=feed_id)

        if feeds.count() > 0:
            feed = feeds[0]

            fs = FileSystemStorage()

            pics = FeedPicture.objects.filter(feed_id=feed.pk)
            for pic in pics:
                fname = pic.picture_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)
                pic.delete()

            fsaves = FeedSave.objects.filter(feed_id=feed.pk)
            for fsave in fsaves:
                fsave.delete()

            fcomments = FeedComment.objects.filter(feed_id=feed.pk)
            for fcomment in fcomments:
                fcomment.delete()

            flikes = FeedLike.objects.filter(feed_id=feed.pk)
            for flike in flikes:
                flike.delete

            if feed.video_url != '':
                fname = feed.video_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)

            feed.delete()

        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def feedLikes(request):
    if request.method == 'POST':
        memberList = []
        feed_id = request.POST.get('feed_id',1)
        member_id = request.POST.get('member_id',1)
        me = Member.objects.get(id=member_id)
        flikes = FeedLike.objects.filter(feed_id=feed_id).order_by('-id')
        for flike in flikes:
            fmember = Member.objects.get(id=flike.member_id)
            memberList.append(fmember)
        serializer = MemberSerializer(memberList, many=True)
        resp = {'result_code': '0', 'data': serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def deleteFeedPicture(request):
    if request.method == 'POST':
        fpic_id = request.POST.get('fpic_id', '1')

        fs = FileSystemStorage()

        pics = FeedPicture.objects.filter(id=fpic_id)
        if pics.count() > 0:
            pic = pics[0]
            feed = Feed.objects.get(id=pic.feed_id)

            if pic.picture_url != '':
                if feed.picture_url == pic.picture_url:
                    fname = feed.picture_url.replace(settings.URL + '/media/', '')
                    fs.delete(fname)
                    feed.picture_url = ''
                    feed.save()
                fname = pic.picture_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)
            pic.delete()

            if feed.picture_url == '':
                pics = FeedPicture.objects.filter(feed_id=feed.pk)
                if pics.count() > 0:
                    pic = pics[0]
                    feed.picture_url = pic.picture_url
                    feed.save()

            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def editFeedPicture(request):
    if request.method == 'POST':
        fpic_id = request.POST.get('fpic_id', '0')
        feed_id = request.POST.get('feed_id',1)
        member_id = request.POST.get('member_id',1)

        if int(fpic_id) > 0:

            pics = FeedPicture.objects.filter(id=fpic_id)

            fs = FileSystemStorage()

            if pics.count() > 0:
                pic = pics[0]
                feed = Feed.objects.get(id=pic.feed_id)

                try:
                    ps = request.FILES.getlist('pictures')
                    for f in ps:
                        filename = fs.save(f.name, f)
                        uploaded_url = fs.url(filename)

                        if pic.picture_url != '':
                            if feed.picture_url == pic.picture_url:
                                fname = feed.picture_url.replace(settings.URL + '/media/', '')
                                fs.delete(fname)
                                feed.picture_url = ''
                                feed.save()
                            fname = pic.picture_url.replace(settings.URL + '/media/', '')
                            fs.delete(fname)

                        pic.picture_url = settings.URL + uploaded_url
                        pic.save()

                        if feed.picture_url == '':
                            feed.picture_url = pic.picture_url
                            feed.save()

                except MultiValueDictKeyError:
                    print('no picture uploaded')

                resp = {'result_code':'0'}

            else:
                resp = {'result_code':'1'}

        else:

            feeds = Feed.objects.filter(id=feed_id)

            fs = FileSystemStorage()

            if feeds.count() > 0:
                feed = feeds[0]

                try:
                    ps = request.FILES.getlist('pictures')
                    for f in ps:
                        filename = fs.save(f.name, f)
                        uploaded_url = fs.url(filename)

                        p = FeedPicture()
                        p.feed_id = feed.pk
                        p.member_id = member_id
                        p.picture_url = settings.URL + uploaded_url
                        p.save()

                        if feed.picture_url == '':
                            feed.picture_url = p.picture_url
                            feed.save()

                except MultiValueDictKeyError:
                    print('no picture uploaded')

                resp = {'result_code':'0'}

            else:
                resp = {'result_code':'1'}

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def updatefeed(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '1')
        member_id = request.POST.get('member_id',1)
        description = request.POST.get('description', '')
        privacy = request.POST.get('privacy', '')
        location = request.POST.get('location', '')
        latitude = request.POST.get('latitude', '0')
        longitude = request.POST.get('longitude', '0')

        feeds = Feed.objects.filter(id=feed_id)
        if feeds.count() == 0:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))
        feed = feeds[0]
        feed.description = description
        feed.privacy = privacy
        feed.location = location
        feed.latitude = latitude
        feed.longitude = longitude

        fs = FileSystemStorage()
        try:
            video = request.FILES['video']
            thumb = request.FILES['thumb']

            if feed.picture_url != '':
                fname = feed.picture_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)

            if feed.video_url != '':
                fname = feed.video_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)

            filename = fs.save(video.name, video)
            uploaded_url = fs.url(filename)
            feed.video_url = settings.URL + uploaded_url
            filename = fs.save(thumb.name, thumb)
            uploaded_url = fs.url(filename)
            feed.picture_url = settings.URL + uploaded_url

        except MultiValueDictKeyError:
            print('no video uploaded')

        feed.save()

        try:
            ps = request.FILES.getlist('pictures')
            i = 0
            for f in ps:
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                p = FeedPicture()
                p.feed_id = feed.pk
                p.member_id = member_id
                p.picture_url = settings.URL + uploaded_url
                p.save()
                if i == 1:
                    if feed.picture_url == '':
                        feed.picture_url = settings.URL + uploaded_url
                        feed.save()

        except MultiValueDictKeyError:
            print('no picture uploaded')

        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))






































