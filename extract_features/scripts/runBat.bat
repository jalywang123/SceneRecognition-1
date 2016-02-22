@echo off

for %%v in ("C:\Users\Johnny\Desktop\extract_features\scripts\runTest\*.bat") do (
echo %%v 
call "%%v"
) 

pause

	