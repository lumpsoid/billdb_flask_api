import pytest
from billdb_flask_api.app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DATABASE_PATH": "../bills.db"
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

def test_qr(client):
    # Simulate a POST request with JSON data
    data = {
        'link': 'https://suf.purs.gov.rs/v/?vl=A0tCNk5ZQ0FRVDg0WEwyTzD%2FbAAARQgAAGBV7AMAAAAAAAABi02%2BdwkCAABGlRNCZvaa5T6pTJsamBVo3NEkwM3yboEA0h4Kxc5t%2F42RN0V%2B6evWH8fWx0o4nvpqSb%2B%2FEo70p5DYU%2BUzjYHJFMJwwy%2B1EF9ePYIu6mjtGGjv%2BgP8ZDXj%2BO4mqqJavL0BLizdY6ixBxPTC3tZx0y3U4%2BUNDDQ6VtLigni86w5iwRs%2F8hpwt5DoEdqqQp8dQDf4CLe6F5KeDsGHYsvXRwyqWJ22FVimmUneK%2B92pyTKNPsdQJ1tgbBeLRvYog5Mfx2V2dK4Cbb0YPWESXZ146plM1%2B2YfgUaItZTsinp0dd%2BU4x9j%2BOfdYy0C0VP46WNfna5QvSzyep6PBjTRM6kbRjEZCKuMrcrjENRUaTc7Nd%2BdQ60zjpDQT4Qtg7UcJnN3hItkEj7CFyZlaYb7pEJ66gsMtmcKMyjIvEIHjPDHw55nDzig9dSfZalHkGx%2BgFZfXCnDRsvlBWoiPT5MIdP0J5PeEgVvlRtvPXAqxX%2BfNpWyx6lDG0x2PeMvubPHpzCO0mhGsTUq9fTJaxdldg8I33BalRBRLm96AmCqtaB6Eca5wpkvgsIsNpi7EkE1eGyEY1G8Bf5fDlzOlO%2FUNmhyhmnSen9HBwY9TVR2z9%2Bb7c8G3wQhu0DXvGIgfdDyKfEmVYRtaCeDHrh65Wz2pcASI%2B%2FPZpftE38fl5WNLwUsHFYApFv6tSZ8R2AEqYoi9rNg%3D',
        'force': 'false'
    }
    response = client.post('/api/flutter/qr', json=data, content_type='application/json')
    print(response.get_data(as_text=True))

    # Assert that the response status code is 200
    assert response.status_code == 200

    # # Assert that the response JSON contains the expected message
    # assert response.get_json() == {'message': 'Hello, World!'}