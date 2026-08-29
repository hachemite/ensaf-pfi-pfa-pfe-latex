@echo off
setlocal
echo ===================================================
echo   Creation de l'archive Overleaf (ENSAF)
echo ===================================================

python zip_for_overleaf.py overleaf_ensaf_template.zip

if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCES] L'archive overleaf_ensaf_template.zip est prete !
    echo.
) else (
    echo.
    echo [ERREUR] La creation de l'archive a echoue.
    echo.
)
pause
