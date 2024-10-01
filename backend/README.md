## Setup (Local and Production)
```bash
python3 -m venv .backend-venv
pip install -r requirements.txt
```
If you get the following error from the `pip install`:
```
ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.
```
Go into `.backend-venv/pyvenv.vfg`

and set `include-system-site-packages` to `true`.



## Running locally
```bash
source .backend-venv/bin/activate
source ../local-setup.sh
python3 app.py
```

## Running in Production
```bash
source .backend-venv/bin/activate
source ./prod-env.sh
python3 app.py
```