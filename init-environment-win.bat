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
pip install -r requirements-pip.txt

@echo.
@echo -------------------------------------------------------------------------
@echo F I N I S H E D !   L I S T I N G   I N S T A L L E D   P A C K A G E S
pip list

@echo.
@echo -------------------------------------------------------------------------
@echo I N S T A L L I N G   N P M   P A C K A G E S
npm install
pause
