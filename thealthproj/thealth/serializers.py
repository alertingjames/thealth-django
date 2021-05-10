from rest_framework import serializers
from .models import Member, Feed, FeedPicture, FeedComment, IMember

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('__all__')

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('__all__')

class FeedPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedPicture
        fields = ('__all__')

class FeedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedComment
        fields = ('__all__')



########################################################################################## ImageAgent #######################################################################################

class IMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMember
        fields = ('__all__')
















































