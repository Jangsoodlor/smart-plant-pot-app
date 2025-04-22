# Smart Plant Pot 🪴🌊
This project aims to help users monitor the status of their plants by providing current and historical readings of soil moisture, temperature, light, and weather conditions. It also provides a prediction of soil moisture and how long it will take until the plant needs to be watered.

- For micropython code used for data collection, please refer to [knilios/SmartPlantPot](https://github.com/knilios/SmartPlantPot).
- For more information about the predicion model, please refer to [Jangsoodlor/smart-plant-pot-model](https://github.com/Jangsoodlor/smart-plant-pot-model).

## Features
- APIs
    - `/sensor/latest`: Get the latest sensor data.
    - `/sensor/aggregate`: Get aggregated historical data based on “hours” and “days” parameters.
    - `/weather/latest`: Get the latest weather data.
    - `/weather/aggregate`: Get aggregated historical data based on “hours” and “days” parameters.
    - `/predictmoisture/{moisture}`: Get soil moisture prediction for the next 7 days.
- Visualisation
    - Charts for historical sensor and weather data.
    - Visualisation of soil moisture prediction.
- Others
    - See latest sensor readings and current weather conditions.

## Installation
We assumed that you've [set up the database](https://github.com/Jangsoodlor/smart-plant-pot-app/wiki/Database-Schema-&-Setup) before installing the app.
The full the installation guide and basic trobleshooting is available [here](https://github.com/Jangsoodlor/smart-plant-pot-app/wiki/Installation-Guide).
1. Clone this repository, or download it as a zip file and extract it.
1. Go to `api` directory and copy `config.py.example` to `config.py`.
1. Edit `config.py`. Fill in your credentials and follow all the instructoins.
1. (Optional, but recommended) [Create python virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) and [activate it](https://docs.python.org/3/library/venv.html#how-venvs-work).
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

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
