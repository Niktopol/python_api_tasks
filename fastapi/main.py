from fastapi import FastAPI
from routes import get_db
import models
from graphql_schemas import Query, Mutation
from routes import router
from config import engine
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

models.Base.metadata.create_all(bind=engine)

schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema=schema, context_getter=lambda: {'db': next(get_db())})
app = FastAPI()

app.include_router(router, prefix="/api", tags=["book"])
app.include_router(graphql_app, prefix='/graphql')


