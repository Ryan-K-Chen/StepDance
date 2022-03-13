@echo off
    echo NOTICE: Make sure to run batch file as administrator    
    set source= %~dp0.
    set /p target= "Enter the path to the Arduino libraries directory: "
    set exclude= 


::  these commands try to remove folders along with symlinks. fix it somehow???
    forfiles /P "%target%" /C "cmd /c if %errorlevel% == 0 echo @fname is a symlink"
    forfiles /P "%target%" /C "cmd /c if %errorlevel% == 1 echo @fname is a not a symlink"
    forfiles /P "%target%" /C "cmd /c if %errorlevel% == 0 rmdir @path & echo @fname removed"


    forfiles /P "%source%" /C "cmd /c if @isdir==TRUE ( mklink /d \"%target%\@file\" @path )"
    forfiles /P "%source%\Sensors" /C "cmd /c if @isdir==TRUE ( mklink /d \"%target%\@file\" @path )"
    forfiles /P "%source%\ExternalLibraries" /C "cmd /c if @isdir==TRUE ( mklink /d \"%target%\@file\" @path )"
    forfiles /P "%source%\ControlLibraries" /C "cmd /c if @isdir==TRUE ( mklink /d \"%target%\@file\" @path )"
    forfiles /P "%source%\Utility" /C "cmd /c if @isdir==TRUE ( mklink /d \"%target%\@file\" @path )"

::    cmd /c rmdir %target%\Sensors
::    cmd /c rmdir %target%\ExternalLibraries
::    cmd /c rmdir %target%\ControlLibraries
::    cmd /c rmdir %target%\Utility
    cmd /c rmdir %target%\.git

cmd /k