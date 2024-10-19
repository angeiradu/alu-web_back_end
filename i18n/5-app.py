#!/usr/bin/env python3
"""
A Basic flask application
"""
from typing import (
    Dict, Union
)

from flask import Flask, g, request
from flask import render_template
from flask_babel import Babel


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


@babel.localeselector
def get_locale() -> str:
    """
    Gets locale from request object or user preferences
    """
    # First, check if locale is passed in the request arguments
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale

    # Next, check if the logged-in user has a preferred locale
    if g.user and g.user.get('locale') in Config.LANGUAGES:
        return g.user['locale']

    # Finally, fallback to the best match from the accept-language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": None, "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id) -> Union[Dict[str, Union[str, None]], None]:
    """
    Validate user login details
    Args:
        id (str): user id
    Returns:
        (Dict): user dictionary if id is valid else None
    """
    return users.get(int(id), None)


@app.before_request
def before_request():
    """
    Adds valid user to the global session object `g`
    """
    user_id = request.args.get('login_as')
    if user_id:
        setattr(g, 'user', get_user(user_id))
    else:
        setattr(g, 'user', None)


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders a basic html template
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run()
