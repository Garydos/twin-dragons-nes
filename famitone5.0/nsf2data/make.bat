@echo off
@echo Please enter any hex numbers with the prefix '0x' instead of '$'
@echo.
set /p dpcm_addr="Enter the base address of your DPCM samples (listed as FT_DPCM_OFF in famitone5.s)[default=0xfc00]: "
IF "%dpcm_addr%"=="" (
    SET dpcm_addr=0xfc00
)
set /p base_addr="Enter starting address for your sfx data (where it will be placed in ROM)[default=0xee00]: "
IF "%base_addr%"=="" (
    SET base_addr=0xee00
)
set /A dpcm_addr=%dpcm_addr%
set /A "ft_dpcm_ptr=(%dpcm_addr%&0x3fff)>>6"
rem @echo %ft_dpcm_ptr%
@echo.
@echo Converting .nsf to .asm...
@echo.
.\nsf2data5.exe %1 -ca65
@IF ERRORLEVEL 1 GOTO failure
@echo.
@echo Compiling...
ca65 -D FT_DPCM_PTR=%ft_dpcm_ptr% %~n1.s -o %~n1.o
@IF ERRORLEVEL 1 GOTO failure
@echo.
@echo Linking...
ld65 -S %base_addr% -o %~n1.bin -C linker_conf_nsf2data.cfg %~n1.o
@IF ERRORLEVEL 1 GOTO failure
@del %~n1.o
@del %~n1.s
@echo.
@echo Success!
@pause
@GOTO endbuild
:failure
@echo.
@echo Build error!
@pause
:endbuild
