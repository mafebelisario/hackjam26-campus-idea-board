import tempfile
import unittest
from pathlib import Path
from app import create_app

class IdeaBoardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({"TESTING": True, "DATABASE": str(Path(self.temp.name) / "test.db")})
        self.client = self.app.test_client()
    def tearDown(self): self.temp.cleanup()
    def test_home(self): self.assertEqual(self.client.get('/').status_code, 200)
    def test_create_and_persist(self):
        payload = {"title":"Campus Recycling", "description":"Find bins around USF", "category":"Off the Grid"}
        response = self.client.post('/api/ideas', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get('/api/ideas').json[0]['title'], payload['title'])
        self.assertEqual(self.client.post('/api/ideas/1/upvote').json['votes'], 1)
        self.assertEqual(self.client.get('/api/ideas').json[0]['votes'], 1)
    def test_invalid_input(self):
        self.assertEqual(self.client.post('/api/ideas',json={"title":"X","description":"hello","category":"Home Turf"}).status_code,400)
        self.assertEqual(self.client.post('/api/ideas',json={"title":"Good idea","description":"Nice idea","category":"Wrong"}).status_code,400)
        self.assertEqual(self.client.post('/api/ideas/999/upvote').status_code,404)
if __name__ == '__main__': unittest.main()
