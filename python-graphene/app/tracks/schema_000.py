import graphene
from graphene_django import DjangoObjectType
from .models import Track
"""
It is 4th section 10th video code
"""


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class Query(graphene.ObjectType):
    # to get all tracks as list
    # we will a list of data that confirms exactly
    # to how our Track was modeled
    tracks = graphene.List(TrackType)

    def resolve_tracks(self, info):
        return Track.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user or None
        track = Track(title=title, description=description,
                      url=url, posted_by=user)
        # save track in database
        track.save()
        return CreateTrack(track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, url, description):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Log in to add a track")

        track = Track(title=title, description=description,
                      url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)

        # # getting current user from context
        # user = info.context.user or None
        # # we are updating a track as we want to make sure that ,
        # # user updating a given track is the one that is created it.
        # # we will find the individual track , by track_id
        # # provided by its arguments
        # track = Track.objects.get(id=track_id)
        # # we can get the information who created the given track from
        # # the posted_by field and that’s going to come from
        # # the track that we found according to its id.
        # if track.posted_by != user:
        #     raise Exception("Not permitted to update this track.")
        # track.title = title
        # track.description = description
        # track.url = url

        # track.save()
        # return UpdateTrack(track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
