@echo off
setlocal
echo ===================================================
echo   Compilation du Rapport de Stage (ENSAF / Rassil)
echo ===================================================

set TECTONIC_PATH=%USERPROFILE%\.tectonic_bin\tectonic.exe

if exist "%TECTONIC_PATH%" (
    echo Compilation avec Tectonic portable...
    "%TECTONIC_PATH%" main.tex
) else (
    where pdflatex >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        echo Compilation avec pdflatex...
        pdflatex -synctex=1 -interaction=nonstopmode main.tex
        bibtex main
        pdflatex -synctex=1 -interaction=nonstopmode main.tex
        pdflatex -synctex=1 -interaction=nonstopmode main.tex
    ) else (
        echo [ERREUR] Aucun compilateur detecte.
        echo Lancez 'python preview.py' pour initialiser le compilateur automatique.
        pause
        exit /b 1
    )
)

if exist "main.pdf" (
    echo.
    echo [SUCCES] main.pdf genere avec succes !
    echo.
) else (
    echo.
    echo [ECHEC] La compilation a echoue. Verifiez les logs.
    echo.
)
