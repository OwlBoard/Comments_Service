import strawberry
from strawberry.fastapi import GraphQLRouter

# Define un tipo básico para GraphQL.
# En el futuro, aquí podrías definir un tipo `CommentType`
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, GraphQL!"

# Crea el esquema de Strawberry
schema = strawberry.Schema(query=Query)

# Crea la aplicación/router de GraphQL que se importará en app.py
graphql_app = GraphQLRouter(schema)