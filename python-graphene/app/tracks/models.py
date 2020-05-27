from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Track(models.Model):
    # maximum length of title is 50 characters
    title = models.CharField(max_length=50)
    # description can be null in database
    description = models.TextField(blank=True)
    # it is charfield with some url validation
    url = models.URLField()
    # automatically set time to now
    created_at = models.DateTimeField(auto_now_add=True)
    # to get information who posted it
    # to include this put user information on posted_by
    # we are going to need a foreign key
    # and this foreign key allows us to specify a many to one relationship
    # so for many tracks we have created they can all point to one user
    # CASCADE means when an object that is referenced by a foreign key is deleted ,
    # here given user is deleted (it is cascade delete ), the entire track that is
    # associated with it be deleted too.
    posted_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)


class Like(models.Model):
    # using models.Model we can create database table
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
    # tracks.Track accessing Track model
    # related_name means we allow when we query for tracks we are going to
    # allow them to get information about the likes  that have been put on a track
    # (in the same sense likes will be able to have information
    # about the track that was liked)
    # each track will be able to have information about the likes that it has on it.
    #  we want "related_name" field on tracks when we query for tracks to be called likes
    track = models.ForeignKey(
        'tracks.Track', related_name='likes', on_delete=models.CASCADE)
