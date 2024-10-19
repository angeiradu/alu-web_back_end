#!/usr/bin/env python3
"""
A Basic flask application
"""
import pytz
import datetime
from typing import Dict, Union
from flask import Flask, g, request, render_template
from flask_babel import Babel, format_datetime


class Config(object):
    """
    Application configuration class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Instantiate the application object
app = Flask(__name__)
app.config.from_object(Config)

# Wrap the application with Babel
babel = Babel(app)

# Define the users table globally
users: Dict[int, Dict[str, Union[str, None]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: Union[str, int]) -> Union[Dict[str, Union[str, None]], None]:
    """
    Retrieve user by ID from the users table
    """
    try:
        return users.get(int(user_id))
    except (ValueError, TypeError):
        return None


@babel.localeselector
def get_locale() -> str:
    """
    Gets the best locale from the request, user preference, or defaults
    """
    # List of options to select locale from: request, user, or default
    locale_options = [
        request.args.get('locale', '').strip(),  # Locale from query parameters
        g.user.get('locale') if g.user else None,  # Locale from user data
        request.accept_languages.best_match(app.config['LANGUAGES']),  # From browser
        Config.BABEL_DEFAULT_LOCALE  # Default locale
    ]
    
    # Return the first valid locale in the options list
    for locale in locale_options:
        if locale in Config.LANGUAGES:
            return locale
    return Config.BABEL_DEFAULT_LOCALE


@babel.timezoneselector
def get_timezone() -> str:
    """
    Retrieves the timezone from the request or user data
    """
    timezone = request.args.get('timezone', '').strip()
    
    # Use user's timezone if available
    if not timezone and g.user:
        timezone = g.user.get('timezone')
    
    # Ensure timezone is valid, else fallback to default
    try:
        pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        timezone = Config.BABEL_DEFAULT_TIMEZONE
    
    return timezone


@app.before_request
def before_request() -> None:
    """
    Function to run before each request. It sets the user and current time.
    """
    user_id = request.args.get('login_as')
    g.user = get_user(user_id)  # Set the user in the global context
    g.time = format_datetime(datetime.datetime.now())  # Set current time


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders the homepage using a basic template
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
