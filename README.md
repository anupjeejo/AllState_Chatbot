->Install and Run Ollama version gemma3:4b on local

------------------------
#CLI Commands
------------------------

->create virtual environment:
	python -m venv venv

->Activate venv:
	>Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
	>venv\Scripts\Activate.ps1

->Install requirements from requirements file: 
  pip install -r requirements.txt

->Run StreamLit app
	streamlit run app.py
