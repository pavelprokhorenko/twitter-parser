# Twitter parser

## Installing

* pre-commit hook.

```bash
$ pre-commit install
```

* install requirements.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
* You should create "settings.yaml" in root, copy "settings.yaml.example" into "settings.yaml" and specify credentials.

## Run server

```bash
$ python main.py
```

## Documentation

* API docs (swagger) you can see on `http://<Service Host>/docs`
