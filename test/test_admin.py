def test_admin_list_clients_correct(auth_client, create_user):
    user = create_user(username="admin", password="admin", role="admin")
    user2 = create_user(username="adam", password="adam", role="client", client_balance=400)
    c = auth_client(user)

    response = c.get("/admin/clients")

    assert response.status_code == 200

    data = response.json()["items"]
    assert data[1]["balance"]=="400.00"

def test_admin_list_clients_incorrect_role(auth_client, create_user):
    user = create_user(username="admin", password="admin", role="client")
    c = auth_client(user)
    response = c.get("/admin/clients")
    assert response.status_code == 403

    # data = response.json()
    # assert data[]

def test_admin_list_users_correct(create_user, auth_client):
    admin = create_user(username="admin", password="admin", role="admin")
    c = auth_client(admin)
    create_user(username="adam", password="adam", role="client")
    response = c.get("/admin/users")
    assert response.status_code == 200
    data = response.json()["items"]
    assert data[1]["username"] == "adam"

def test_admin_list_users_incorrect_role(create_user, auth_client):
    admin = create_user(username="admin", password="admin", role="admin")
    user2 = create_user(username="adam", password="adam", role="client")
    c = auth_client(user2)
    response = c.get("/admin/users")
    assert response.status_code == 403

def test_admin_list_transactions_correct(create_user, auth_client):
    admin = create_user(username="admin", password="admin", role="admin")
    user2 = create_user(username="adam", password="adam", role="client")

    c = auth_client(user2)
    response = c.post("/transactions/", json={
        "transaction_type": "deposit",
        "amount": 200
    })

    assert response.status_code==200
    c = auth_client(admin)

    response = c.get("/admin/transactions")
    assert response.status_code == 200

    data = response.json()["items"]
    assert data[0]["amount"] == "200.00"


def test_admin_list_transactions_incorrect_role(create_user, auth_client):
    admin = create_user(username="admin", password="admin", role="admin")
    user2 = create_user(username="adam", password="adam", role="client")

    c = auth_client(user2)
    response = c.post("/transactions/", json={
        "transaction_type": "deposit",
        "amount": 200
    })

    assert response.status_code==200

    response = c.get("/admin/transactions")
    assert response.status_code == 403



def test_admin_get_client_by_id_correct(create_user, auth_client):

    user = create_user(username="adam", password="adam", role="client", client_balance=500)
    admin = create_user(username="admin", password="admin", role="admin")
    c = auth_client(admin)
    response = c.get("/admin/clients/1")

    assert response.status_code == 200

    data = response.json()
    assert data["balance"] == "500.00"

def test_admin_get_client_by_id_incorrect_role(create_user, auth_client):
    user = create_user(username="adam", password="adam", role="client", client_balance=500)
    admin = create_user(username="admin", password="admin", role="admin")
    c = auth_client(user)
    response = c.get("/admin/clients/1")
    assert response.status_code == 403

def test_admin_get_client_by_id_incorrect_id(create_user, auth_client):
    user = create_user(username="adam", password="adam", role="client", client_balance=500)
    admin = create_user(username="admin", password="admin", role="admin")
    c = auth_client(admin)
    response = c.get("/admin/clients/3")
    assert response.status_code == 404

def test_admin_delete_user_by_username_correct(create_user, auth_client):
    user = create_user(username="adam", password="adam", role="client", client_balance=500)
    admin = create_user(username="admin", password="admin", role="admin")
    c = auth_client(admin)
    response = c.delete("/admin/users/adam")
    assert response.status_code == 204

def test_admin_delete_user_by_username_incorrect_role(create_user, auth_client):
    user = create_user(username="adam", password="adam", role="client", client_balance=500)
    admin = create_user(username="admin", password="admin", role="admin")
    c = auth_client(user)
    response = c.delete("/admin/users/adam")
    assert response.status_code == 403

def test_admin_delete_user_by_username_incorrect_username(create_user, auth_client):
    user = create_user(username="adam", password="adam", role="client", client_balance=500)
    admin = create_user(username="admin", password="admin", role="admin")
    c = auth_client(admin)
    response = c.delete("/admin/users/notfound")
    assert response.status_code == 404


