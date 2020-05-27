import graphene
import tracks.schema
import users.schema
import graphql_jwt
from graphql import GraphQLError


class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    # this is root query class
    pass


class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    # this is root mutation class
    # consist mutations
    # token_auth gives JWT, if the credentials that we,
    # provide for given user are correct
    # if incorrect it should return an error and no token
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify the token that we got from token auth
    verify_token = graphql_jwt.Verify.Field()
    # we are not going to use this in our app
    refresh_token = graphql_jwt.Refresh.Field()

# added Query and Mutation class to schema
schema = graphene.Schema(query=Query, mutation=Mutation)
