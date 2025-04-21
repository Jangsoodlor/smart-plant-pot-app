# Smart Plant Pot 🪴🌊
This project aims to create a system to notify users when to water their plants.

- For micropython code used for data collection, please refer to [knilios/SmartPlantPot](https://github.com/knilios/SmartPlantPot).
- For the predicion model, please refer to [Jangsoodlor/smart-plant-pot-model](https://github.com/Jangsoodlor/smart-plant-pot-model).

## Features (TBA)
- APIs.
    - `/sensor/latest`: Get the latest sensor data.
    - `/sensor/aggregate`: Get aggregated historical data based on “hours” and “days” parameters.
    - `/weather/latest`: Get the latest weather data.
    - `/weather/aggregate`: Get aggregated historical data based on “hours” and “days” parameters.
- Visualisation.

## Installation
Please refer to [the installation guide](https://github.com/Jangsoodlor/smart-plant-pot-app/wiki/Installation-Guide).

## Usage
### API
1. Start the server
    ```bash
    cd api
    python app.py
    ```
2. Go to `localhost:8080/moisture/v1/ui`.

### Web Application & Visualisation
1. Start the server
    ```bash
    cd frontend
    streamlit run main.py
    ```
2. Go to `http://localhost:8501/`.

### Running tests
```bash
pip install -r test-requirements.txt
cd test
pytest
```
