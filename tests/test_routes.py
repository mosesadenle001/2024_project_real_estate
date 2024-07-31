
def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Properties" in response.data

def test_register_page(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_search_properties(test_client):
    response = test_client.get('/search')
    assert response.status_code == 200
    assert b'Search' in response.data

def test_compare_properties(test_client):
    response = test_client.get('/compare')
    assert response.status_code == 200
    assert b'Compare Properties' in response.data

def test_reset_password(test_client):
    response = test_client.get('/reset_password')
    assert response.status_code == 200
    assert b'Reset Password' in response.data

def test_logout(test_client, login_regular_user):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'You have been logged out.' in response.data

def test_account_page(test_client, login_regular_user):
    response = test_client.get('/account', follow_redirects=True)
    assert response.status_code == 200
    assert b'Account' in response.data



