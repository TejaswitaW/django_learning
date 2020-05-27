import graphene
from graphene_django import DjangoObjectType
# we will just replace Exception with GraphQLError
from graphql import GraphQLError
from django.db.models import Q

from .models import Track, Like
from users.schema import UserType


class TrackType(DjangoObjectType):
    # this is structure of our query
    # this has multiple fields
    class Meta:
        # through this meta class TrackType inherit structure of Track
        model = Track


class LikeType(DjangoObjectType):
    class Meta:
        # this inner class modeled after Like model
        model = Like


class Query(graphene.ObjectType):
    # to get all tracks as list
    # we will a list of data that confirms exactly
    # to how our Track was modeled
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info, search=None):
        # filter is set  conditionally, according to the Q objects
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(url__icontains=search) |
                Q(posted_by__username__icontains=search)
            )
            return Track.objects.filter(filter)
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()


class CreateTrack(graphene.Mutation):
    # we want to return the created track on track field
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to add a track")
            # raise Exception("Log in to add a track")
        track = Track(title=title, description=description,
                      url=url, posted_by=user)
        # save track in database
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        # track_id to figure out which track needs
        # to be updated
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, url, description):
        # grabbing current user from context
        user = info.context.user
        # we are updating a track as we want to make sure that ,
        # user updating a given track is the one that is created it.
        # we will find the individual track , by track_id
        # provided by its arguments
        track = Track.objects.get(id=track_id)
        # we can get the information who created the given track from
        # the posted_by field and that’s going to come from
        # the track that we found according to its id.
        if track.posted_by != user:
            raise GraphQLError("Not permitted to update this track.")
            # raise Exception("Not permitted to update this track.")

        track.title = title
        track.description = description
        track.url = url

        track.save()
        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise GraphQLError("Not permitted to delete this track.")
            # raise Exception("Not permitted to delete this track.")
        track.delete()
        return DeleteTrack(track_id=track_id)


class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        # to create like the only argument we need is the track_id
        # of the user is liking, so we have track_id argument
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login to like tracks.")
            # raise Exception("Login to like tracks.")
        track = Track.objects.get(id=track_id)
        if not track:
            raise GraphQLError("Cannot find track with given track id")
            # raise Exception("Cannot find track with given track id")
        Like.objects.create(
            user=user,
            track=track
        )
        return CreateLike(user=user, track=track)


class Mutation(graphene.ObjectType):
    # we need to register our mutations here
    # because of this step we can see mutation in documentation
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
