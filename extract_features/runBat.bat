@echo off

for %%v in ("C:\Users\Johnny\Desktop\test_tmp\*.bat") do (
echo %%v 
call %%v
) 

pause

	