import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    # this query has multiple fields
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()


class Query(graphene.ObjectType):
    # this is Root query
    # users,hello,is_admin these are the queries
    # we need to register our query here
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    # for each query there is resolver function
    # means for particular query these fuctions will give result
    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="Tejaswita", created_at=datetime.now()),
            User(id="2", username="Nirav", created_at=datetime.now()),
            User(id="3", username="Vikas", created_at=datetime.now()),
            User(id="4", username="Pratik", created_at=datetime.now()),
        ][:limit]


class CreateUser(graphene.Mutation):
    # we want CreateUser return entire user
    # we want to create user dynamically
    user = graphene.Field(User)

    class Arguments:
        # inner class
        username = graphene.String()

    def mutate(self, info, username):
        # creating new user
        # we are not passing id and created_at
        # we want them to be created automatically
        user = User(id="10", username=username, created_at=datetime.now())
        # it returns user
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    # this is root mutation class
    create_user = CreateUser.Field()


# we have provided root query class to schema
schema = graphene.Schema(query=Query, mutation=Mutation)

# here we are executing our query
# means we are writing schema for our query
result = schema.execute(
    # the query we are firing, that query here will get executed
    '''
    
    mutation{
        createUser(username:"Tom"){
            user{
                id
                username
                createdAt
            }
        }
    }
    
    '''
)
print(result.data.items())
dict_result = dict(result.data.items())
print(json.dumps(dict_result))
print(json.dumps(dict_result, indent=2))
