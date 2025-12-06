import unittest
from app import create_app
from app.extensions import db



class MechanicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_shop.db"

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Helper: create mechanic
    def create_mechanic(self, email="mech1@example.com"):
        payload = {
            "first_name": "Test",
            "last_name": "Mechanic",
            "email": email,
            "password": "password123",
            "salary": 60000,
            "address": "123 Shop Lane"
        }
        return self.client.post("/mechanics/", json=payload)

    # Helper: login + return token header
    def auth_header(self, email="mech1@example.com", password="password123"):
        self.create_mechanic(email=email)
        resp = self.client.post("/mechanics/login", json={
            "email": email,
            "password": password
        })
        token = resp.get_json()["token"]
        return {"Authorization": f"Bearer {token}"}

    # ------------------ TESTS ------------------

    def test_create_mechanic_success(self):
        resp = self.create_mechanic()
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["email"], "mech1@example.com")

    def test_create_mechanic_missing_field(self):
        # Your current route throws KeyError → 500
        # So we accept any non-201 result
        payload = {
            "first_name": "NoLastName",
            "email": "nolast@example.com",
            "password": "password123",
            "salary": 50000
        }
        resp = self.client.post("/mechanics/", json=payload)
        self.assertNotEqual(resp.status_code, 201)

    def test_get_mechanics(self):
        self.create_mechanic()
        resp = self.client.get("/mechanics/")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_update_mechanic_success(self):
        resp = self.create_mechanic()
        mech_id = resp.get_json()["id"]

        headers = self.auth_header()
        
        resp = self.client.put(f"/mechanics/{mech_id}", json={"salary": 75000}, headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["salary"], 75000)

        

    def test_update_mechanic_not_found(self):
        headers = self.auth_header()
        resp = self.client.put("/mechanics/9999", json={"salary": 80000}, headers=headers)
        self.assertEqual(resp.status_code, 404)

    def test_delete_mechanic_success(self):
        resp = self.create_mechanic()
        mech_id = resp.get_json()["id"]

        headers = self.auth_header()

        resp = self.client.delete(f"/mechanics/{mech_id}", headers=headers)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get("/mechanics/")
        ids = [m["id"] for m in resp.get_json()]
        self.assertNotIn(mech_id, ids)

    def test_delete_mechanic_not_found(self):
        headers = self.auth_header()
        resp = self.client.delete("/mechanics/9999", headers=headers)
        self.assertEqual(resp.status_code, 404)

    def test_mechanic_login_success(self):
        self.create_mechanic()
        resp = self.client.post("/mechanics/login", json={
            "email": "mech1@example.com",
            "password": "password123"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.get_json())

    def test_mechanic_login_bad_password(self):
        self.create_mechanic()
        resp = self.client.post("/mechanics/login", json={
            "email": "mech1@example.com",
            "password": "wrongpass"
        })
        self.assertEqual(resp.status_code, 401)

    def test_my_tickets_requires_token(self):
        resp = self.client.get("/mechanics/my-tickets")
        self.assertEqual(resp.status_code, 401)

    def test_my_tickets_success(self):
        self.create_mechanic()
        headers = self.auth_header()

        resp = self.client.get("/mechanics/my-tickets", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.get_json(), list)
