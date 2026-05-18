
#	to run only main, run `make main` on cmd
main:
	.venv/Scripts/activate.bat && python app/main.py

#	to run only window, run `make window` on cmd
window:
	.venv/Scripts/activate.bat && python app/window.py

#	to run only source, run `make source` on cmd
source:
	.venv/Scripts/activate.bat && python app/source.py