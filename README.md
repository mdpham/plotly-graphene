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

___


For those without Docker, you'll need to add `virtualenv` to your server directory
`cd server && virtualenv .`
And then run separate make commands for each
`make backend`
`make frontend`

Now we must start up a local minio server and mongodb server.
For Windows Users:
You can modify the `server/run_minio.bat` with the correct paths for the exe file and the data folder. Then double-clicking this will start a minio server.
You can repeat the same process for `server/run_mongodb.bat` and use it similarly.

Alternatively, you can do the following to do things in a more linux fashion
You will have to modify your `server/minio_client/client` file with the appropriate connection details
The Minio command can be uncommented in the Makefile, pointed to the correct paths for `minio.exe` and the minio directory in this repo, and then run
`make minio`
The process for mongodb is also similar
