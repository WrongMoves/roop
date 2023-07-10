@echo off

set APPPATH="C:\Users\allth\Downloads\SD\roop\run.py"
set ENV=roop
set COMMANDLINE_ARGS=--execution-provider cuda --execution-threads 16 --max-memory 64 --frame-processor face_swapper --keep-fps --keep-audio 
call cd "C:\Users\allth\Downloads\SD\roop"
call conda activate %ENV%
call python %APPPATH% %COMMANDLINE_ARGS%