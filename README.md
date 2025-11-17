# Stock Market Tracker

This project is a Django-based web application for monitoring stock prices from the Brazilian market. Users can select stocks, track their key metrics on a dynamic dashboard, and receive email alerts for significant price fluctuations.

## Features

*   **Stock Selection**: Choose from a comprehensive list of stocks available on the Brazilian market, powered by the `investpy` library.
*   **Live Tracking Dashboard**: View key stock metrics, including Open, High, Low, Close, and Volume for your selected stocks.
*   **Custom Refresh Intervals**: Set a custom timer (in minutes) for each stock to define how often its price should be checked for updates.
*   **Email Price Alerts**: Enter your email to receive notifications when a stock's price increases or decreases by more than 40% between checks.

## Technologies Used

*   **Backend**: Python, Django
*   **Frontend**: HTML, CSS, JavaScript, Bootstrap, jQuery, HTMX
*   **Data Source**: `yfinance`, `investpy`
*   **Database**: SQLite

## Setup and Installation

Follow these steps to set up and run the project locally.

**1. Clone the Repository**

```bash
git clone https://github.com/0nerb/StockMarket.git
cd StockMarket
```

**2. Create and Activate a Virtual Environment**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**

Install the required Python packages.

```bash
pip install django yfinance investpy
```

**4. Configure Email Settings**

For the email alert feature to work, you must configure your SMTP settings in `stockproject/settings.py`. Open the file and update the following lines with your email provider's details.

For Gmail, you will need to generate an "App Password".

```python
# stockproject/settings.py

...
#email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com' # CHANGE THIS
EMAIL_HOST_PASSWORD = 'your-google-app-password' # CHANGE THIS
...
```

**5. Apply Database Migrations**

Run the following command to set up the SQLite database schema.

```bash
python manage.py migrate
```

**6. Start the Development Server**

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## How to Use

1.  Navigate to the home page (`http://127.0.0.1:8000/`).
2.  Select one or more stocks from the list that you wish to track.
3.  Enter your email address in the email form at the bottom of the page to enable price alerts.
4.  Click the first "Submit" button to go to the tracking dashboard.
5.  On the dashboard, you will see a table with your selected stocks. For each stock, enter an update interval in minutes into the "Timer" input field and click the adjacent "Submit" button.
6.  The timer will start, and the application will check for price updates at the specified interval. If a stock's price changes by more than 40% (either up or down) from its last checked value, an alert will be sent to the email address you provided.
