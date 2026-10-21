@echo off
echo Testing Prospector AI API...
echo.
echo 1. Testing health endpoint...
curl http://localhost:8000/health
echo.
echo.
echo 2. Testing research endpoint...
echo (This will take 30-60 seconds...)
curl -X POST http://localhost:8000/api/v1/research -H "Content-Type: application/json" -d "{\"company_url\":\"chat360.io\"}"
echo.
echo Done!
pause
