@REM windows .bat 

@REM USE:
@REM with PowerShell or Command Prompt: devscripts\windows\run_windows_docker.bat

docker-compose -f docker-compose-dev.yml build 
docker-compose -f docker-compose-dev.yml up 
