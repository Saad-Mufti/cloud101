## Setup
```
npm install
```

## Running locally
```bash 
npm i
source ../local-setup.sh
npm run start
```

## Deploying to App Engine
1. Change the service in `app.yaml` to your name like so: `first-last`. This ensures there won't be any name collisions

2. Run `gcloud app deploy`