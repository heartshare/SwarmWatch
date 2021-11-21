@echo off

echo [1m[+] Activating virtual environment.[0m
call %0\..\venv\scripts\activate
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Upgrading pip.[0m
pip install --upgrade pip --quiet
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Removing stale packaging directories, if they exist.[0m
for %%d in ("build" "dist" ".mypy_cache") do (
   echo - Removing %%~d directory.
   rd /s /q "%%~d" 2>nul
)

echo [1m[+] Validating requirements, install/upgrade as necessary.[0m
for %%d in ("isort" "pyquotes" "mypy" "wheel") do (
   echo - %%~d.
   pip install "%%~d" --quiet --upgrade
)
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Running isort in check mode.[0m
isort --check SwarmWatch setup.py
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Running pyquotes in check mode.[0m
pyquotes --check SwarmWatch setup.py
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Running mypy in check mode.[0m
mypy SwarmWatch
if %errorlevel% neq 0 goto :ERROR

echo [1m[+] Building wheel.[0m
python setup.py bdist_wheel
if %errorlevel% neq 0 goto :ERROR

echo [92m[+] Packaging SwarmWatch is complete.[0m
goto :CLEANUP

:ERROR
echo [91m[!] Packaging SwarmWatch has failed.[0m

:CLEANUP
echo [1m[+] Cleaning up.[0m
for %%d in ("build" ".mypy_cache") do (
   echo - Removing %%~d directory.
   rd /s /q "%%~d" 2>nul
)

echo [1m[+] Press any key to exit.[0m
pause >nul