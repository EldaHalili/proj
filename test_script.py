import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index_route(self):
        # Test the index route '/'
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sticky Notes App', response.data)

    def test_add_note_route(self):
        # Test the add_note route '/add_note'
        data = {
            'note_text': 'Test note',
            'note_color': 'yellow'
        }
        add_response = self.app.post('/add_note', json=data)
        self.assertEqual(add_response.status_code, 200)
        self.assertIn(b'Note created successfully', add_response.data)
        new_note_id = add_response.json['note_id']

        # Test the delete_note route '/delete_note/<int:note_id>'
        response = self.app.post(f'/delete_note/{new_note_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Note deleted successfully', response.data)

if __name__ == '__main__':
    unittest.main()
