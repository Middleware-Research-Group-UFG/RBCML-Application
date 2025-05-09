# Contextualizing
This application proceeds with the work done by [Victor Netto](https://github.com/VictorNetto) in [PFC](https://github.com/VictorNetto/PFC). It intents to generalize the application by providing users flexibility to create models and sessions following the [Role-based Communication Modeling Language](https://repositorio.bc.ufg.br/tede/items/6ae6f1a4-8e17-440a-aed6-f5efc94c3950). It also aims to add new features.
  <details>
  <summary>  <strong> New features </strong> </summary>
    
- **Database:** to store models, sessions and users.
- **Authentication:** to securely identify who is accessing the application.
- **Invitation sistem:** to invite users to be part of a session. 

</details>

## How to run
### Project clone
```bash
git clone git@github.com:Middleware-Research-Group-UFG/RBCML-Application.git
```

### Create virtual environment
```bash
python3 -m venv environment
```

###  Activate virtual environment
```bash
source environment/bin/activate
```

### Change directory
```bash
cd RBCML-Application/
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Initialize database
```bash
sqlite3 app/database/rbcml.db <  app/database/schema.sql
```

### Run
```bash
python3 run.py
```
