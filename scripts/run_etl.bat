@echo off
chcp 65001 > nul
cd /d %~dp0

:: Ghi thời gian bắt đầu vào log
echo [%DATE% %TIME%] Bắt đầu quá trình ETL >> etl_log.txt

echo [1/3] extract.py >> etl_log.txt
"C:\Program Files\Python313\python.exe" extract.py >> etl_log.txt 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [%DATE% %TIME%] Lỗi extract.py >> etl_log.txt
    exit /b 
)

echo [2/3] transform.py >> etl_log.txt
"C:\Program Files\Python313\python.exe" transform.py >> etl_log.txt 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [%DATE% %TIME%] Lỗi transform.py >> etl_log.txt
    exit /b 
)

echo [3/3] load.py >> etl_log.txt
"C:\Program Files\Python313\python.exe" load.py >> etl_log.txt 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [%DATE% %TIME%] Lỗi load.py >> etl_log.txt
    exit /b
)

echo [%DATE% %TIME%] ETL hoàn tất thành công >> etl_log.txt
exit /b
