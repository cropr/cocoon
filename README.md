# Development Cocoon website

## Front End

- cd cocoon_frontend
- yarn dev


## Back End

- cd cocoon_backend
- ./launchlocal

# Deploymemnt Settings cocoon website

## App Engine

- go to https://console.cloud.google.com/appengine?project=cocoon-kosk and create the app   engine with Python

## Google sign in

- go to https://console.cloud.google.com/apis/dashboard?project=cocoon-kosk and select Crendentials
- click "+ create credentials", select "OAuth client ID", and then "Web Application"
- Fill in form:
  - Name: Cocoon
  - Javascript origin 1: "https://cocoon.kosk.be"
  - Javascript origin 2: "http://localhost:3000"
  - Javascript origin 2: "http://localhost"
- Copy Client ID to  backend/app.yaml and to frontend/pages/mgmt/mgmt.index and to backend/cocoon/settings.py

## Secrets

- go to https://console.cloud.google.com/apis/dashboard?project=cocoon-kosk ans select APIs and services
- enable Secret Manager API if not enabled yet
- go to https://console.cloud.google.com/security/secret-manager?referrer=search&project=cocoon-kosk
- create the secrets and upload the scretes values from /shared/secrets
- go to https://console.cloud.google.com/iam-admin/iam?project=cocoon-kosk and add role Secret Manager Secret Accessor to service account cocoon-kosk@appspot.gserviceaccount.com

## Upload new version of application 

In frontend directory

```bash
API_URL=https://cocoon.kosk.be/ yarn generate
gcloud app deploy
```

In backend directory

```bash
gcloud app deploy
```

## 1 time actions after 1ste version app is uploaded

in root directory

```bash
gcloud app dispatch.yml
```

For the mapping of cocoon.kosk.be go to https://console.cloud.google.com/appengine/settings/domains/add?project=cocoon-kosk