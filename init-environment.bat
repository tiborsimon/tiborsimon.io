virtualenv site-env
call activate
pip install pip-tools
rm -f requirements.txt
pip-compile
pip-sync
pause