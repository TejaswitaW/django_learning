import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    # this query is with multiple subfields
    # for such queries we have to create seperate class
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()


class Query(graphene.ObjectType):
    # this is Root query
    # users query returns list of users
    # structure of each user is passed by passing User
    users = graphene.List(User)
    # these are simple queries , which return single value
    # with single data type
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info):
        # resolver for users
        return [
            User(id="1", username="Tejaswita", created_at=datetime.now()),
            User(id="2", username="Nirav", created_at=datetime.now()),
            User(id="3", username="Vikas", created_at=datetime.now()),
            User(id="4", username="Pratik", created_at=datetime.now()),
        ]


schema = graphene.Schema(query=Query)
result = schema.execute(
    # we need to specify subfields for each users data
    '''
    {
        users{
            id
            username
            createdAt
        }
    }
    '''
)
print(result.data.items())
dict_result = dict(result.data.items())
print(json.dumps(dict_result))
print(json.dumps(dict_result, indent=2))
