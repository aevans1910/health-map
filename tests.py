from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_provider_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_provider = {
    'title': 'DDS',
    'name': 'Rones',
    'location': '555 Post St',
    'phone' : '415 890 4589'}

sample_form_data = {
    'title': sample_provider['title'],
    'name': sample_provider['name'],
    'location': sample_provider['location'],
    'phone': sample_provider['phone']
}
class ProvidersTests(TestCase):

    def setUp(self):
        """Stuff to do before every test"""
        #Get the Flask test client
        self.client = app.test_client() 

        #Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the providers homepage"""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Provider', result.data)

    def test_new(self):
        """Test the new provider creation page"""
        result = self.client.get('/providers/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New provider', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_provider(self, mock_find):
        """Test editing a single profile"""
        mock_find.return_value = sample_provider

        result = self.client.get(f'/providers/{sample_provider_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'DDS', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_provider(self, mock_find):
        """Test showing a single provider"""
        mock_find.return_value = sample_provider

        result = self.client.get(f'/providers/{sample_provider_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'DDS', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_provider(self, mock_insert):
        """Test submitting a new profile"""
        result = self.client.post('/providers', data=sample_form_data)

        #After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_provider)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_provider(self, mock_update):
        result = self.client.post(f'/providers/{sample_provider_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_provider_id}, {'$set': sample_provider})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_provider(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/providers/{sample_provider_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_provider_id})

if __name__ == '__main__':
    unittest_main()
