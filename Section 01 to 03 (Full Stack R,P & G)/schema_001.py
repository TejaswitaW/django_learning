import graphene
import json


class Query(graphene.ObjectType):
    hello = graphene.String()
    # query to check user is a administrator or not
    # which results in either true of false
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        # this function should prepended with resolve and in snake case
        return "world"

    def resolve_is_admin(self, info):
        # resolver function for is_admin query
        return True


schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query,auto_camelcase=False)
result = schema.execute(
    # graphQL operations need to be in camel case
    # else you will get an error
    '''
    {
        isAdmin
    }
    '''
)
print(result.data.items())
dict_result = dict(result.data.items())
print(json.dumps(dict_result))
print(json.dumps(dict_result, indent=2))
