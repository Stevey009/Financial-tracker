import os
import tempfile
import pytest
from app import app, db, Transaction

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_index_page(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Transactions' in resp.data


def test_add_transaction(client):
    resp = client.post('/add', data={
        'description': 'Coffee',
        'amount': '3.5',
        'type': 'expense'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Coffee' in resp.data
