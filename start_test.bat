call venv\Scripts\activate.bat
pip install -r requirements.txt
pytest -k "test_async_functions"
pause