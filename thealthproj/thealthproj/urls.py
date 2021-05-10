from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from thealth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^thealth/', include('thealth.urls')),
    url(r'^imageagent/', include('imageagent.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^signup',views.signup,  name='signup'),
    url(r'^signin',views.signin,  name='signin'),
    url(r'^forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'^vcoderesend', views.vcoderesend, name='vcoderesend'),
    url(r'^sendvcode', views.sendvcode, name='sendvcode'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    url(r'^rstpwd', views.rstpwd, name='rstpwd'),
    url(r'^codesubmit', views.codesubmit, name='codesubmit'),
    url(r'^resendcode', views.resendcode, name='resendcode'),
    url(r'^registerprofile', views.registerProfile, name='registerProfile'),
    url(r'^pwdreset', views.pwdreset, name='pwdreset'),
    url(r'^postnewfeed', views.postnewfeed, name='postnewfeed'),
    url(r'^homefeeds', views.homefeeds, name='homefeeds'),
    url(r'^likeFeed',views.likeFeed,  name='likeFeed'),
    url(r'^unLikeFeed',views.unLikeFeed,  name='unLikeFeed'),
    url(r'^saveFeed',views.saveFeed,  name='saveFeed'),
    url(r'^unSaveFeed',views.unSaveFeed,  name='unSaveFeed'),
    url(r'^feedFollow',views.feedFollow,  name='feedFollow'),
    url(r'^feedUnfollow',views.feedUnfollow,  name='feedUnfollow'),
    url(r'^getFeedPictures',views.getFeedPictures,  name='getFeedPictures'),
    url(r'^getFeedComments',views.getFeedComments,  name='getFeedComments'),
    url(r'^sendFeedComment',views.sendFeedComment,  name='sendFeedComment'),
    url(r'^delFeed',views.delFeed,  name='delFeed'),
    url(r'^feedLikes',views.feedLikes,  name='feedLikes'),
    url(r'^deleteFeedPicture',views.deleteFeedPicture,  name='deleteFeedPicture'),
    url(r'^editFeedPicture',views.editFeedPicture,  name='editFeedPicture'),
    url(r'^updatefeed',views.updatefeed,  name='updatefeed'),
]


urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns=format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





























