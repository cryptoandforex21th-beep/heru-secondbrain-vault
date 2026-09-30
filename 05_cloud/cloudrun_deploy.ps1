# Skrip Deploy ke Google Cloud Run
# Pastikan Google Cloud SDK (gcloud) sudah terpasang dan login (gcloud auth login)

param (
    [string]$ProjectID = "YOUR_GCP_PROJECT_ID",
    [string]$ServiceName = "secondbrain-portal",
    [string]$Region = "asia-southeast2" # Jakarta
)

Write-Host "🚀 Menyiapkan Deployment ke Google Cloud Run ($Region)..." -ForegroundColor Cyan

# 1. Pastikan project aktif
gcloud config set project $ProjectID

# 2. Build & Deploy via Cloud Run
gcloud run deploy $ServiceName `
    --source . `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --set-env-vars GEMINI_API_KEY="YOUR_KEY_OR_SECRET"

Write-Host "✅ Selesai! Web App SecondBrain Anda sudah online di Cloud Run." -ForegroundColor Green
