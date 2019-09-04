from graphene_django import DjangoObjectType
import graphene
from .models import Track


class TrackType(DjangoObjectType):
    class Meta:
        model = Track

class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)
    def resolve_tracks(self, info):
        return Track.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, title, description):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('First Login In to create a track')
        track = Track(title=title, description= description, posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.String(required=True)
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, track_id, title, description):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user != track.posted_by:
            raise Exception('Not permitted to update this track')
        track.title = title
        track.description = description
        track.save()
        return UpdateTrack(track=track)

class DeleteTrack(graphene.Mutation):
    track_id = graphene.String()
    class Arguments:
        track_id = graphene.String()
    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user !=track.posted_by:
            raise Exception('Not permitted to update this track')
        track.delete()
        return DeleteTrack(track_id=track_id)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
