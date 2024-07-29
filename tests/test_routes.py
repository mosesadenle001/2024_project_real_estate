
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

def test_logout(test_client, login_regular_user):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data  # Check that we are redirected to the login page
    assert b'You have been logged out.' in response.data  # Check for the flash message

def test_account_page(test_client, login_regular_user):
    response = test_client.get('/account', follow_redirects=True)
    assert response.status_code == 200
    assert b'Account' in response.data

def test_admin_dashboard_access_denied(test_client, login_regular_user):
    response = test_client.get('/admin')
    assert response.status_code == 403

def test_admin_dashboard_access_granted(test_client, login_admin_user):
    response = test_client.get('/admin')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_list_users_admin(test_client, login_admin_user):
    response = test_client.get('/admin/users')
    assert response.status_code == 200
    assert b'List of Users' in response.data

def test_update_user_admin(test_client, login_admin_user):
    response = test_client.get('/admin/user/1/update')
    assert response.status_code == 200
    assert b'Admin Update User' in response.data

def test_update_property_admin(test_client, login_admin_user):
    response = test_client.get('/property/update/1')
    assert response.status_code == 200
    assert b'Update Property' in response.data

def test_add_property(test_client, login_regular_user):
    response = test_client.get('/add_property')
    assert response.status_code == 200
    assert b'New Property' in response.data

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
