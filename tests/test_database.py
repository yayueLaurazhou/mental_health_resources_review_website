import unittest
from app import app
from app import db, Resources, Reviews

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def test_resource_creation(self):
        with app.app_context():
            resource = Resources(name="test_resource", description="123")
            db.session.add(resource)
            db.session.commit()

            retrieved_resource = Resources.query.filter_by(name="test_resource").first()

        self.assertIsNotNone(retrieved_resource)
        self.assertEqual(retrieved_resource.description, "123")

    def test_comment_creation(self):
        with app.app_context():
            resource = Resources(name="test_resource", description="123")
            db.session.add(resource)
            db.session.commit()

            review = Reviews(rating="test_user", content="345", resource_id=resource.id)
            db.session.add(review)
            db.session.commit()

            retrieved_review = Reviews.query.filter_by(resource_id=resource.id).first()

        self.assertIsNotNone(retrieved_review)
        self.assertEqual(retrieved_review.content, "345")


    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()