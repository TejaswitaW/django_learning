from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # these are the things those are strictly necessary
        # only_fields = ("id", "email", "password")


class Query(graphene.ObjectType):
    # as we are querying user by id so passed id
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    # following is the query
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    # arguments necessary to create new user

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        # get_user_model() creates user
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    # we have created mutation
    create_user = CreateUser.Field()
