@echo off
SET PROJECT_ID=project-44f98a7a-8bb4-4edc-ac1
SET REGION=asia-southeast1
SET SERVICE_NAME=whatsapp-cloud-bot
SET JOB_NAME=wa-glo-mbg-morning-job

echo [1/3] Enabling required Google Cloud APIs...
cmd /c "gcloud services enable run.googleapis.com cloudbuild.googleapis.com cloudscheduler.googleapis.com --project %PROJECT_ID%"

echo [2/3] Deploying Cloud Run Service...
cmd /c "gcloud run deploy %SERVICE_NAME% --source . --region %REGION% --allow-unauthenticated --project %PROJECT_ID%"

echo [3/3] Setting up Cloud Scheduler trigger for 07:00 AM daily...
cmd /c "gcloud scheduler jobs create http %JOB_NAME% --schedule="0 7 * * *" --time-zone="Asia/Makassar" --uri="https://%SERVICE_NAME%-%REGION%.run.app/send-scheduled-msg" --http-method=POST --project %PROJECT_ID%"

echo Done!
