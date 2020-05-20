import graphene
import json


class Query(graphene.ObjectType):
    # this class is subclass of graphene.ObjectType
    # this is root query type
    # hello is field for our query
    hello = graphene.String()

    def resolve_hello(self, info):
        # this is specific to GraphQL operation
        # which resolves the operation
        # its name should start with resolve
        # its name should be in snake case
        return "world"


# creating schema based off of a root query type
# we pass Query class to Schema
schema = graphene.Schema(query=Query)
# executing hello query
# storing return value in result
result = schema.execute(
    # passing graphQL operation as a string
    '''
    {
        hello
    }
    '''
)
# returned dictionary
print(result.data.items())
# performing operation hello which return world
print(result.data["hello"])
dict_result = dict(result.data.items())
# put result in json format
print(json.dumps(dict_result))
print(json.dumps(dict_result, indent=2))
