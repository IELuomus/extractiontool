# windows .ps1

# USE:
# have .env in extractiontool/ root ( check devscripts/.env-file-example )
# with Powershell: PowerShell.exe -ExecutionPolicy Bypass -File devscripts/windows/run_windows_docker.ps1

docker-compose -f docker-compose-dev.yml build 
docker-compose -f docker-compose-dev.yml up 
