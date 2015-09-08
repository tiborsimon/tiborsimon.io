@echo off
@echo.
@echo "Creating virtual env in folder site-env.."
virtualenv site-env

@echo.
@echo "Activating virtual environment.."
call activate

@echo.
@echo "Installing pip-tools.."
pip install pip-tools

@echo.
@echo "Removing old requirements.txt file.."
rm -f requirements.txt

@echo.
@echo "Compile requirements.."
pip-compile

@echo.
@echo "Syncing requirements.."
pip-sync

@echo.
@echo "Finished! Listing installed packages.."
pip list
pause