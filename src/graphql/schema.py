import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, GraphQL!"

schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)