@echo off

cd scripts


echo Installing requirements...

pip install -r requirements.txt >> nul

if %errorlevel%==1 (
	echo Failed to install requirements!
	pause
	exit /B 1
)

echo Requirements installed successfully!


echo Running script...
python main.py


pause