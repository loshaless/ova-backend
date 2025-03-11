## activate environment
```bash
source .venv/bin/activate 
```

## Install the package
```bash
pip install -r requirements.txt
``` 

## update the package
```bash
pip freeze > requirements.txt
``` 

## start development server
```bash
cd src
uvicorn app.main:app --workers 4
```

# NOTES
don't for get to add env
