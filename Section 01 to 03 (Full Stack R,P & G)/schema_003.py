import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()


class Query(graphene.ObjectType):
    # this is Root query
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        # same as previous py file only added limit argument
        # to get specified number of users
        # we have made limit value optional
        return [
            User(id="1", username="Tejaswita", created_at=datetime.now()),
            User(id="2", username="Nirav", created_at=datetime.now()),
            User(id="3", username="Vikas", created_at=datetime.now()),
            User(id="4", username="Pratik", created_at=datetime.now()),
        ][:limit]


schema = graphene.Schema(query=Query)
result = schema.execute(
    '''
    {
        users(limit:2){
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
