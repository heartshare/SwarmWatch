@echo off

echo [1m[+] Activating virtual environment.[0m
call %0\..\venv\scripts\activate
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Upgrading pip.[0m
pip install --upgrade pip --quiet
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Validating requirements, install/upgrade as necessary.[0m
for %%d in ("twine") do (
   echo - %%~d.
   pip install "%%~d" --quiet --upgrade
)
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Running twine check.[0m
twine check dist/*
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Uploading packages.[0m
twine upload --config-file SwarmWatch.pypirc --repository pypi dist/*
if %errorlevel% neq 0 goto :ERROR

echo [92m[+] Publishing is complete.[0m
goto :CLEANUP

:ERROR
echo [91m[!] Publishing has failed.[0m

:CLEANUP
echo [1m[+] Removing packages.[0m
rd /s /q dist 2>nul

echo [1m[+] Press any key to exit.[0m
pause >nul