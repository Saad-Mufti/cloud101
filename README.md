# Cloud 101
## Session 1

In our first workshop, we'll be covering 3 tools in GCP (which have similar equivalents on Azure and AWS):

1. Using App Engine as a serverless platform to deploy applications

2. Setting up a scalable SQL PostgreSQL database with CloudSQL

3. Using Cloud VM to run the backend that lets our website talk to our PostgreSQL db

### Setup
We'll be doing everything on [Replit](), an online IDE which lets us operate without having to deal with dependency issues (although, it may be worthwhile to try this later on your local machine since Replit's free tier is somewhat limiting).

Instructions for the frontend, backend, and database are in their respective folders.

#### Logging into Google Cloud SDK
```bash
gcloud auth login --no-launch-browser
gcloud init
```