@echo off
@echo -------------------------------------------------------------------------
@echo C R E A T I N G   V I R T U A L   E N V I R O N M E N T
virtualenv site-env

@echo.
@echo -------------------------------------------------------------------------
@echo A C T I V A T I N G   V I R T U A L   E N V I R O N M E N T
call activate

@echo.
@echo -------------------------------------------------------------------------
@echo I N S T A L L I N G   P I P - T O O L S
pip install pip-tools

@echo.
@echo -------------------------------------------------------------------------
@echo R E M O V I N G   O L D   R E Q U I R E M E N T S . T X T   F I L E
rm -f requirements.txt

@echo.
@echo -------------------------------------------------------------------------
@echo C O M P I L E   R E Q U I R E M E N T S
pip-compile

@echo.
@echo -------------------------------------------------------------------------
@echo S Y N C I N G   R E Q U I R E M E N T S
pip-sync

@echo.
@echo -------------------------------------------------------------------------
@echo F I N I S H E D !   L I S T I N G   I N S T A L L E D   P A C K A G E S
pip list
pause