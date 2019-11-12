@echo off
@echo Please enter any hex numbers with the prefix '0x'
@echo.
set /p dpcm_addr="Enter the base address of your DPCM samples (listed as FT_DPCM_OFF in famitone5.s)[default=0xfc00]: "
IF "%dpcm_addr%"=="" (
    SET dpcm_addr=0xfc00
)
set /p base_addr="Enter starting address for your music data (where it will be placed in ROM)[default=0xcac0]: "
IF "%base_addr%"=="" (
    SET base_addr=0xcac0
)
set /A dpcm_addr=%dpcm_addr%
set /A "ft_dpcm_ptr=(%dpcm_addr%&0x3fff)>>6"
@echo.
@echo Converting .txt to .asm...
@echo.
.\text2data.exe %1 -ca65
@IF ERRORLEVEL 1 GOTO failure
@echo.
@echo Compiling...
ca65 -D FT_DPCM_PTR=%ft_dpcm_ptr% %~n1.s -o %~n1.o
@IF ERRORLEVEL 1 GOTO failure
@echo.
@echo Linking...
ld65 -S %base_addr% -o %~n1.bin -C linker_conf_text2data.cfg %~n1.o
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
@echo Build error!
@echo If you get a "Range error", it's likely that you didn't allocate enough space for your samples.
@echo Rerun this script with the same file and a lower DPCM sample address until it compiles successfully.
@pause
:endbuild
