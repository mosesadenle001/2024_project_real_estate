# Real Estate Listings Platform

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone https://github.com/mosesadenle001/real_estate
    cd real_estate
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```sh
    flask run
    ```

## Docker Instructions

1. **Build and run the application using Docker**:
    ```sh
    docker-compose build
    docker-compose up
    ```

2. **Access the application**:
    Open your browser and go to `http://localhost:5000`.

## Usage

### Export Property Data

- To export property data to CSV format, go to `http://localhost:5000/export`.

## Deployment

### Deploying to Heroku

1. **Create a Heroku app**:
    ```sh
    heroku real_estate_listings_platform
    ```

2. **Deploy the application**:
    ```sh
    git push heroku main
    ```

3. **Set environment variables on Heroku**:
    ```sh
    heroku config:set FLASK_APP=run.py FLASK_ENV=production
    ```

4. **Access your application**:
    Open your browser and go to `https://real_estate_listings_platform.herokuapp.com`.

