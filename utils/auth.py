import os
import flask
import requests
import threading

import google.oauth2.credentials
import google_auth_oauthlib.flow

from utils.bot import Bot

# This OAuth 2.0 access scope allows for read access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/tasks.readonly'
]


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


class FlaskThread(threading.Thread):
    def __init__(self, host: str = "localhost", port: int = 1234) -> None:
        super().__init__()
        self.app = None
        self.host = host
        self.port = port

    def run(self) -> None:
        self.app.run(self.host, port=self.port)


def create_app(bot: Bot, secret_file: str = "credentials.json"):
    app = flask.Flask(__name__)
    app.secret_key = 'iUZ14ULwgRya5cMjf2zQVZqGhXv0qULNvCSXFWvrTNA='

    @app.route('/authorize')
    def authorize():
        # Create flow instance to manage the OAuth 2.0
        # Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            secret_file, scopes=SCOPES)

        flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token
            access_type='offline',
            # Enable incremental authorization.
            include_granted_scopes='true')

        # Store the state so the callback can verify the auth server response.
        flask.session['state'] = state

        return flask.redirect(authorization_url)

    @app.route('/oauth2callback')
    def oauth2callback():
        # Specify the state when creating the flow in the callback so that it
        # can verified in the authorization server response.
        state = flask.session['state']

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            secret_file, scopes=SCOPES, state=state)
        flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

        # Use the authorization server's response to fetch the OAuth 2.0 token.
        authorization_response = flask.request.url
        flow.fetch_token(authorization_response=authorization_response)

        # Store credentials in the session.
        credentials = flow.credentials
        flask.session['credentials'] = credentials_to_dict(credentials)

        bot.connect_service(credentials)

        # Save credentials back to session in case access token was refreshed.
        flask.session['credentials'] = credentials_to_dict(credentials)

        return "Succesfully logged !"

    @app.route('/revoke')
    def revoke():
        if 'credentials' not in flask.session:
            return ('You need to <a href="/authorize">authorize</a> before ' +
                    'testing the code to revoke credentials.')

        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])

        revoke = requests.post(
            'https://oauth2.googleapis.com/revoke',
            params={'token': credentials.token},
            headers={
                'content-type': 'application/x-www-form-urlencoded'
            }
        )

        status_code = getattr(revoke, 'status_code')
        if status_code == 200:
            bot.disconnect_service()
            return 'Credentials successfully revoked.'
        else:
            return 'An error occurred.'

    @app.route('/clear')
    def clear_credentials():
        if 'credentials' in flask.session:
            del flask.session['credentials']

        bot.disconnect_service()
        return 'Credentials have been cleared.<br><br>'

    # TODO: remove
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    return app
