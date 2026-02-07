@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Done! Virtual environment is ready.
echo To activate it manually, run: venv\Scripts\activate
