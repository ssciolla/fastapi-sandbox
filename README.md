# Fast API sandbox

GitHub repo for experimenting with Fast API and SQLModel

## Installation and Usage

```
python3 -m venv venv
source venv/bin/activate  # Mac OS
pip install -r requirements.txt
uvicorn cars.main:app --reload
uvicorn sandbox.main:app --reload
```