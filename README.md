# plotly-graphene
More intern boilerplate for CReSCENT, plotly visualization refactoring effort
* use react hooks
* use apollo hooks
* use graphene with minio and loompy

`cp sample.env .env`

`docker build -t plotly-graphene-server server`

`docker build -t plotly-graphene-client client`

`docker-compose up`

Go to `localhost:9000` for minio and `localhost:8000` for graphql playground and `localhost:3000` for react app.
