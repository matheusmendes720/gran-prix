@echo off
REM Git Workflow Script for Nova Corrente Project

echo ===================================
echo Nova Corrente Git Workflow Helper
echo ===================================

if "%1"=="" goto help

if "%1"=="setup" goto setup_project
if "%1"=="feature" goto create_feature_branch
if "%1"=="bugfix" goto create_bugfix_branch
if "%1"=="release" goto prepare_release
if "%1"=="merge-feature" goto merge_feature_to_develop
if "%1"=="merge-release" goto merge_release_to_main
if "%1"=="help" goto help

echo Unknown command: %1
goto help

:create_feature_branch
echo Creating a new feature branch...
set /p feature_name="Enter feature name (e.g., user-authentication): "
git checkout develop
git pull origin develop
git checkout -b feature/%feature_name%
echo Created and switched to branch: feature/%feature_name%
goto :eof

:create_bugfix_branch
echo Creating a new bugfix branch...
set /p bug_name="Enter bug description (e.g., fix-login-error): "
git checkout develop
git pull origin develop
git checkout -b bugfix/%bug_name%
echo Created and switched to branch: bugfix/%bug_name%
goto :eof

:prepare_release
echo Creating a new release branch...
set /p release_version="Enter release version (e.g., v1.2.0): "
git checkout develop
git pull origin develop
git checkout -b release/%release_version%
echo Created and switched to branch: release/%release_version%
echo Remember to update version numbers in package.json, etc.
goto :eof

:merge_feature_to_develop
echo Merging current feature branch to develop...
for /f %%i in ('git branch --show-current') do set current_branch=%%i

if not "%current_branch%" == "feature" (
    echo Error: You must be on a feature branch to merge to develop
    exit /b 1
)

git checkout develop
git pull origin develop
git merge %current_branch% --no-ff
echo Merged %current_branch% to develop
goto :eof

:merge_release_to_main
echo Merging release branch to main...
for /f %%i in ('git branch --show-current') do set current_branch=%%i

if not "%current_branch%" == "release" (
    echo Error: You must be on a release branch to merge to main
    exit /b 1
)

git checkout main
git pull origin main
git merge %current_branch% --no-ff
echo Merged %current_branch% to main

REM Create tag
set release_version=%current_branch:release/=%
git tag -a %release_version% -m "Release %release_version%"
echo Created tag: %release_version%
goto :eof

:setup_project
echo Setting up project branches...

REM Create main branch if it doesn't exist
git checkout -b main 2>nul || git checkout main

REM Create develop branch if it doesn't exist
git checkout -b develop 2>nul || git checkout develop

REM Set up remote tracking
git push -u origin main
git push -u origin develop

echo Project branches set up successfully!
goto :eof

:help
echo Available commands:
echo   setup          - Initialize project branches
echo   feature        - Create a new feature branch
echo   bugfix         - Create a new bugfix branch
echo   release        - Create a new release branch
echo   merge-feature  - Merge current feature to develop
echo   merge-release  - Merge current release to main
echo   help           - Show this help