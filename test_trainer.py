from re import M
import unittest
import os
import json
import io
from datetime import datetime

from app import create_app, db
from app.models import Trainer


class TrainerTestCase(unittest.TestCase):
    """This class represents the trainer test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.trainer_csv = "tests/trainer.csv"

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_upload_trainer_data(self):
        """Test API can upload Trainer CSV (POST request)"""
        with open(self.trainer_csv, "rb") as f:
            res = self.client().post(
                "/upload/",
                content_type="multipart/form-data",
                data={"data": f, "type": "trainer"},
            )

        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class PokemonTestCase(unittest.TestCase):
    """This class represents the pokemon test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.pokemon_csv = "tests/pokemon.csv"
        self.trainer = {
            "id": "trainer1",
            "firstName": "Ash",
            "lastName": "Cathem",
            "dateOfBirth": datetime.strptime("22-05-1987", "%d-%m-%Y").date(),
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            self._add_trainer()

    def _add_trainer(self, commit=True):
        """Setup trainer data inside test_db"""
        db.session.add(Trainer(**self.trainer))

        if commit:
            db.session.commit()

    def test_upload_pokemon_data(self):
        """Test API can upload Pokemon CSV (POST request)"""
        with open(self.pokemon_csv, "rb") as f:
            res = self.client().post(
                "/upload/",
                content_type="multipart/form-data",
                data={"data": f, "type": "pokemon"},
            )

        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # def test_trainer_creation(self):
    #     """Test API can create a trainer (POST request)"""
    #     res = self.client().post("/trainers/", data=self.trainer)
    #     self.assertEqual(res.status_code, 201)
    #     self.assertIn("Go to Borabora", str(res.data))

    # def test_api_can_get_all_trainers(self):
    #     """Test API can get a trainer (GET request)."""
    #     res = self.client().post("/trainers/", data=self.trainer)
    #     self.assertEqual(res.status_code, 201)
    #     res = self.client().get("/trainers/")
    #     self.assertEqual(res.status_code, 200)
    #     self.assertIn("Go to Borabora", str(res.data))

    # def test_api_can_get_trainer_by_id(self):
    #     """Test API can get a single trainer by using it's id."""
    #     rv = self.client().post("/trainers/", data=self.trainer)
    #     self.assertEqual(rv.status_code, 201)
    #     result_in_json = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    #     result = self.client().get("/trainers/{}".format(result_in_json["id"]))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn("Go to Borabora", str(result.data))

    # def test_trainer_can_be_edited(self):
    #     """Test API can edit an existing trainer. (PUT request)"""
    #     rv = self.client().post("/trainers/", data={"name": "Eat, pray and love"})
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.client().put(
    #         "/trainers/1", data={"name": "Dont just eat, but also pray and love :-)"}
    #     )
    #     self.assertEqual(rv.status_code, 200)
    #     results = self.client().get("/trainers/1")
    #     self.assertIn("Dont just eat", str(results.data))

    # def test_trainer_deletion(self):
    #     """Test API can delete an existing trainer. (DELETE request)."""
    #     rv = self.client().post("/trainers/", data={"name": "Eat, pray and love"})
    #     self.assertEqual(rv.status_code, 201)
    #     res = self.client().delete("/trainers/1")
    #     self.assertEqual(res.status_code, 200)
    #     # Test to see if it exists, should return a 404
    #     result = self.client().get("/trainers/1")
    #     self.assertEqual(result.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()