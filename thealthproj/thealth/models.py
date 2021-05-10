from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    auth_status = models.CharField(max_length=30)
    picture_url = models.CharField(max_length=1000)
    address = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    registered_time = models.CharField(max_length=50)
    followings = models.CharField(max_length=11)
    followers = models.CharField(max_length=11)
    posts = models.CharField(max_length=11)
    status = models.CharField(max_length=20)


class Code(models.Model):
    member_id = models.CharField(max_length=11)
    code = models.CharField(max_length=11)
    status = models.CharField(max_length=30)

class Feed(models.Model):
    member_id = models.CharField(max_length=11)
    picture_url = models.CharField(max_length=1000)
    video_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    privacy = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    posted_time = models.CharField(max_length=50)
    likes = models.CharField(max_length=11)
    comments = models.CharField(max_length=11)
    is_liked = models.CharField(max_length=10)
    is_saved = models.CharField(max_length=10)
    status = models.CharField(max_length=20)


class FeedPicture(models.Model):
    feed_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    picture_url = models.CharField(max_length=1000)


class FeedComment(models.Model):
    feed_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    comment = models.CharField(max_length=1000)
    commented_time = models.CharField(max_length=50)

class FeedLike(models.Model):
    feed_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    liked_time = models.CharField(max_length=50)

class FeedSave(models.Model):
    feed_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    saved_time = models.CharField(max_length=50)

class FeedFollow(models.Model):
    member_id = models.CharField(max_length=11)
    follower_id = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)




########################################################################################## ImageAgent #######################################################################################

class IMember(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)






































