# Development Cocoon website

## Front End

Initial setup: 
```
cd frontend; yarn ; cd ..
```

Launch the frontend:
```
poe fe_run
```
## Back End

Initial setup

```
poetry install
```

Launch the backend

```
poe be_run
```
# Deployment Settings cocoon website

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
- Copy Client ID to  backend/app.yaml and to frontend/nux.config.js and to backend/cocoon/settings.py

## Send email

- go to https://console.cloud.google.com/apis/dashboard?project=cocoon-kosk and select Crendentials
- click 'Manage Service account' and then 'Create service account'
    name: sendemail
    add role: Editor
- return to Credentials screen and click the newly created service account, go to the Keys tab and create a new key
- go to https://admin.google.com and select Security / Access and data control / API controls. 
- Select manage domain-wide delegation, Click Add new, provide client id from key downloaded and add https://www.googleapis.com/auth/gmail.send as scope

## Secrets

- go to https://console.cloud.google.com/apis/dashboard?project=cocoon-kosk ans select APIs and services
- enable Secret Manager API if not enabled yet
- go to https://console.cloud.google.com/security/secret-manager?referrer=search&project=cocoon-kosk
- create the secrets and upload the scretes values from /shared/secrets
- go to https://console.cloud.google.com/iam-admin/iam?project=cocoon-kosk and add role Secret Manager Secret Accessor to service account cocoon-kosk@appspot.gserviceaccount.com

## Upload new version of application 

Generate the new frontend (if changed)

```
poe fe_generate
```

Deploy a new version
```
poe deploy
```

For the mapping of cocoon.kosk.be go to https://console.cloud.google.com/appengine/settings/domains/add?project=cocoon-kosk

