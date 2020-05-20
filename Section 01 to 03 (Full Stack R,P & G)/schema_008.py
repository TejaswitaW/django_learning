import graphene
import json
import uuid
from datetime import datetime


class Post(graphene.ObjectType):
    # fields in post
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    # this query has multiple fields
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())


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
    user = graphene.Field(User)
    # inner class

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        # creating new user
        # we are not passing id and created_at
        # we want them to be created automatically
        user = User(username=username)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    # to indicate shape, Post is passed
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        # print(info.context.get('is_anonymous'))
        # using info we can grab the value provided on context
        # it is a dictionary
        if info.context.get('is_anonymous'):
            raise Exception("Not Authenticated!")
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    # this is mutation class
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


# we have provided root query class to schema
schema = graphene.Schema(query=Query, mutation=Mutation)

# here we are executing our query
# means we are writing schema for our query
result = schema.execute(
    # the query we are firing, that query here will get executed
    # query getUsersQuery($limit:Int){
    '''
   
    mutation {
        createPost(title:"Hello", content:"People"){
            post{
                title
                content
            }
        }
    }
    
    ''',
    context={'is_anonymous': True}

)
print(result.data.items())
dict_result = dict(result.data.items())
print(json.dumps(dict_result))
print(json.dumps(dict_result, indent=2))
