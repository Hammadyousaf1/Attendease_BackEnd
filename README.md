uvicorn app.main:app --reload
pip install -r requirements.txt
uvicorn app.main:app --host 192.168.100.6 --port 8000 --reload

