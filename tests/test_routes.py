import unittest
from app import app


class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        tester = app.test_client(self)
        response = tester.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_add_resource(self):
        tester = app.test_client(self)
        response = tester.post("/add", data={
            "name": "Flask",
            "description": "123",
        })
        assert response.status_code == 200
        
    # No matter the form is valid or not, it will return 200. 
    # If the form is not valid, it will reload the page again.
    def test_add_comment(self):
        tester = app.test_client(self)
        response = tester.post("/comment/2", data={
            "name": "Flask",
            "description": "123",
        })
        assert response.status_code == 200

    def test_invalid_form_submit(self):
        tester = app.test_client(self)
        response = tester.post("/add", data={
            "name": "",
            "description": "123",
        })
        assert response.status_code == 200
        
if __name__ == '__main__':
    unittest.main()