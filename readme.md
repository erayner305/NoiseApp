In order to run, create python virtual environment (https://docs.python.org/3/library/venv.html or if you have VSCode do Ctrl+Shift+P and type create virtual env, specifcally .venv)

Enter that virtual environment and add flask (source .venv/Scripts or something similar/activate, (it might be worth googling how to activate it) then do flask --debug run). It will launch on localhost:5000 so type that into your web browser. Any edits you make will automatically appear in your browser when you refresh the page.

All logic can be funneled into app.py (which is the driver file) via imports.