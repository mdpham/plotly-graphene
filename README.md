# plotly-graphene
More intern boilerplate for CReSCENT, plotly visualization refactoring effort
* use react hooks
* use apollo hooks
* use graphene with minio and loompy

## Docker Setup

`cp sample.env .env`

`docker build -t plotly-graphene-server server`

`docker build -t plotly-graphene-client client`

`docker-compose up`

Go to `localhost:9000` for minio and `localhost:8000` for graphql playground and `localhost:3000` for react app.

___

## No Docker Setup

You'll need to add `virtualenv` to your server directory
`cd server && virtualenv .`
And then run separate make commands for each
`make backend`
`make frontend`

### To start up a local minio server and mongodb server.

You can download the 64-bit version of minio.exe from [here](https://dl.min.io/server/minio/release/windows-amd64/minio.exe)

Go [here](https://docs.mongodb.com/guides/server/install/) to download and install MongoDB. Make sure to customize installation and uncheck install as a Windows Service. The bin folder of the installation directory should have a mongod.exe file whose path you need to know.

#### For Windows Users:

You can modify the `server/run_databases.bat` with the correct paths for the exe files and the data folders for minio and mongodb. Then double-clicking this will start a minio server and a mongodb server in sperate commmand shells.

#### The Linux way

Alternatively, you can do the following to do things in a more linux fashion
You will have to modify your `server/minio_client/client` file with the appropriate connection details
The Minio command can be uncommented in the Makefile, pointed to the correct paths for `minio.exe` and the minio directory in this repo, and then run
`make minio`
The process for mongodb is also similar

### Setup for loom

Because the loom files cannot be read through minio, please make a `{runID}/SEURAT/frontend_normalized` folder structure in server. This structure will be in the docker container so must be emulated (albeit painfully).

## How to use server code

Look at [`server/schema/text/py`](https://github.com/mdpham/plotly-graphene/blob/prab/graphene/server/schema/test.py) for examples of queries.
