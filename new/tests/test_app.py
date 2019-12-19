import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

    rv = login(client, flaskr.app.config['EMAIL'], flaskr.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, flaskr.app.config['EMAIL'] + 'x', flaskr.app.config['PASSWORD'])
    assert b'Invalid password' in rv.data

    rv = login(client, flaskr.app.config['EMAIL'], flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data



