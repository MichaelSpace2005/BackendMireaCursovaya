@echo off
REM Check project structure and key files exist

echo Checking project structure...
echo.

set valid=1

REM Check key files
if not exist "app\main.py" (
    echo ERROR: app\main.py not found
    set valid=0
)

if not exist "app\entities\mechanic.py" (
    echo ERROR: app\entities\mechanic.py not found
    set valid=0
)

if not exist "app\entities\link.py" (
    echo ERROR: app\entities\link.py not found
    set valid=0
)

if not exist "app\entities\user.py" (
    echo ERROR: app\entities\user.py not found
    set valid=0
)

if not exist "app\infra\config.py" (
    echo ERROR: app\infra\config.py not found
    set valid=0
)

if not exist "app\infra\security.py" (
    echo ERROR: app\infra\security.py not found
    set valid=0
)

if not exist "app\infra\database\session.py" (
    echo ERROR: app\infra\database\session.py not found
    set valid=0
)

if not exist "app\infra\database\models.py" (
    echo ERROR: app\infra\database\models.py not found
    set valid=0
)

if not exist "app\infra\repos_impl\mechanic_repo_impl.py" (
    echo ERROR: app\infra\repos_impl\mechanic_repo_impl.py not found
    set valid=0
)

if not exist "app\interfaces\repos\mechanic_repo.py" (
    echo ERROR: app\interfaces\repos\mechanic_repo.py not found
    set valid=0
)

if not exist "docker-compose.yml" (
    echo ERROR: docker-compose.yml not found
    set valid=0
)

if not exist "Dockerfile" (
    echo ERROR: Dockerfile not found
    set valid=0
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found
    set valid=0
)

if not exist "tests\conftest.py" (
    echo ERROR: tests\conftest.py not found
    set valid=0
)

if %valid%==1 (
    echo.
    echo ✓ All required files are present!
    echo.
    echo Project structure is valid
) else (
    echo.
    echo ✗ Some required files are missing!
    exit /b 1
)
