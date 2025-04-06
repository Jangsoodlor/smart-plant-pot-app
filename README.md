# Smart Plant Pot 🪴🌊
This project aims to create a system to notify users when to water their plants.

For code that's used to collect data, please refer to [knilios/SmartPlantPot](https://github.com/knilios/SmartPlantPot).

## Features (TBA)
- API.
- Visualisation.

## Installation
Requirements: You must have python 3 installed on your machine.
1. Clone the repo.
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
1. Go to `api` directory and copy `config.py.example` to `config.py`
1. Edit `config.py` and fill in your credentials.
1. Go to `api/openapi/moisture.yaml`.
1. Copy the contents of `moisture.yaml` and paste it in [Swagger Editor](https://editor.swagger.io/)
1. Click Generate Server -> Python Flask
1. Download and extracts it to `/api/`
1. Rename the newly-extracted folder to whatever you put as `OPENAPI_STUB_DIR` (the default is "stub") in the `config.py` file.

At the end of the installation, your project structure should look something like this:

```
.
├── api/
│   ├── stub/
│   │   ├── swagger_server/
│   │   └── ...
│   ├── config.py
│   └── app.py
├── main.py
├── LICENSE.md
├── README.md
└── ...
```

## Usage
### API
1. Starts the server
    ```bash
    cd ./api
    python app.py
    ```
2. Go to `localhost:8080/moisture/v1/ui`

### Visualisation
TBA.
