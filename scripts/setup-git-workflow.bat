@echo off
REM Setup script for Nova Corrente Git Workflow

echo ===================================
echo Nova Corrente Git Setup
echo ===================================

REM Check if in git repository
if not exist ".git" (
    echo Error: Not in a git repository
    exit /b 1
)

echo Setting up Git workflow for Nova Corrente project...

REM Configure git user.name and user.email if not set
for /f %%i in ('git config user.name 2^>nul') do set git_name=%%i
if "%git_name%"=="" (
    set /p git_name="Enter your name for Git commits: "
    git config user.name "%git_name%"
)

for /f %%i in ('git config user.email 2^>nul') do set git_email=%%i
if "%git_email%"=="" (
    set /p git_email="Enter your email for Git commits: "
    git config user.email "%git_email%"
)

REM Set up branch structure
echo Setting up branch structure...

REM Create main branch if it doesn't exist
git show-ref --verify --quiet refs/heads/main
if errorlevel 1 (
    git checkout -b main
    echo Created main branch
) else (
    echo Main branch already exists
)

REM Create develop branch if it doesn't exist
git show-ref --verify --quiet refs/heads/develop
if errorlevel 1 (
    git checkout -b develop
    echo Created develop branch
) else (
    echo Develop branch already exists
)

REM Configure git settings
echo Applying Git configurations...
git config core.autocrlf true
git config push.default current
git config pull.rebase true

REM Set up remote origin if not set
for /f %%i in ('git remote 2^>nul') do set remote=%%i
if "%remote%"=="" (
    set /p remote_url="Enter remote repository URL: "
    git remote add origin %remote_url%
    echo Added remote origin: %remote_url%
) else (
    echo Remote origin already configured
)

REM Push initial branches
echo Pushing initial branches...
git push -u origin main
git push -u origin develop

echo ===================================
echo Git workflow setup completed!
echo ===================================
echo.
echo Next steps:
echo 1. Create feature branches from 'develop':
echo    git checkout develop ^&^& git pull origin develop
echo    git checkout -b feature/name-of-feature
echo.
echo 2. Follow the workflow documented in docs/GIT_WORKFLOW.md
echo 3. Use conventional commit messages
echo 4. Run tests before pushing
echo.
echo Available git aliases:
echo    git st   - git status
echo    git co   - git checkout
echo    git br   - git branch
echo    git cm   - git commit -m
echo    git tree - git log --oneline --graph --all
echo.