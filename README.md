# cars_price

# install requirments in virtual environments
if there are some issues go to https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

1. python -m venv .venv
2. source .venv/Scripts/activate
3. python -m pip install --upgrade pip
4. python -m pip install -r requirements.txt

# run app
uvicorn fastapi_pred:app --reload

# make prediction
http://127.0.0.1:8000/cars_price
and set all needed informations
and click submit button
