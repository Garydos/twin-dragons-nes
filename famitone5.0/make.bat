@echo off
@echo Please enter any hex numbers with the prefix '0x' instead of '$'
@echo.
set /p base_addr="Enter starting address for famitone5 (where it will be placed in ROM)[default=0xc000]: "
IF "%base_addr%"=="" (
    SET base_addr=0xc000
)
@echo.
@echo Compiling...
ca65 famitone5.s -o famitone5.o 
@IF ERRORLEVEL 1 GOTO failure
@echo.
@echo Linking...
ld65 -S %base_addr% -o .\bin\famitone5.bin -C linker_conf_famitone5.cfg famitone5.o -vm -m .\bin\famitone5.info
@IF ERRORLEVEL 1 GOTO failure
@del famitone5.o
@echo.
@echo Success!
@echo.
@echo See the file 'bin\famitone5.info' for the memory locations of each function
@pause
@GOTO endbuild
:failure
@echo.
@echo Build error!
@pause
:endbuild
