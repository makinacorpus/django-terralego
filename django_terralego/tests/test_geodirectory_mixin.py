import json

from copy import deepcopy

try:
    from unittest import mock
except ImportError:
    import mock

from django.test import TestCase

from django_terralego.tests.models import Dummy

GEOJSON_SAMPLE = {
    "id": "6af234fb-ec81-4189-ab6b-ac9b1483e665",
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [
            -104.590948,
            38.319914
        ]
    },
    "bbox": [
        -104.590948,
        38.319914,
        -104.590948,
        38.319914
    ],
    "properties": {
        "tags": [
            "django_terralego.Dummy",
            "toto"
        ]
    }
}


class GeoDirectoryMixinTest(TestCase):
    """ Test the mixins by mocking the actual requests. """

    @mock.patch('requests.post')
    def test_save_without_geo_info(self, mocked_post):
        dummy = Dummy()
        dummy.save()
        self.assertEqual(mocked_post.call_count, 0)

    @mock.patch('requests.post')
    def test_save_with_geo_info(self, mocked_post):
        mocked_response = mock.MagicMock()
        mocked_response.json.return_value = GEOJSON_SAMPLE
        mocked_post.return_value = mocked_response
        dummy = Dummy()
        dummy.terralego_geometry = 'POINT(-104.590948 38.319914)'
        dummy.save()
        self.assertEqual(dummy.terralego_id, GEOJSON_SAMPLE['id'])
        self.assertEqual(dummy.terralego_geometry, GEOJSON_SAMPLE['geometry'])
        self.assertEqual(dummy.terralego_tags, json.dumps(GEOJSON_SAMPLE['properties']['tags']))
        self.assertEqual(mocked_post.call_count, 1)

    @mock.patch('requests.get')
    def test_retrieve_geo_info(self, mocked_get):
        mocked_response = mock.MagicMock()
        mocked_response.json.return_value = GEOJSON_SAMPLE
        mocked_get.return_value = mocked_response
        dummy = Dummy(terralego_id=GEOJSON_SAMPLE['id'])
        dummy.update_from_terralego_entry()
        self.assertEqual(dummy.terralego_geometry, GEOJSON_SAMPLE['geometry'])
        self.assertEqual(dummy.terralego_tags, json.dumps(GEOJSON_SAMPLE['properties']['tags']))
        self.assertEqual(mocked_get.call_count, 1)

    @mock.patch('requests.post')
    def test_save_without_model_path_in_tags(self, mocked_post):
        mocked_response = mock.MagicMock()
        mocked_response.json.return_value = GEOJSON_SAMPLE
        mocked_post.return_value = mocked_response
        dummy = Dummy()
        dummy.terralego_geometry = 'POINT(-104.590948 38.319914)'
        dummy.terralego_tags = json.dumps([])
        dummy.save()
        self.assertEqual(mocked_post.call_count, 1)
        tags = mocked_post.mock_calls[0][2]['data']['tags']
        self.assertEqual(tags, json.dumps(['django_terralego.Dummy']))

    @mock.patch('requests.post')
    def test_save_with_model_path_in_wrong_position_in_tags(self, mocked_post):
        mocked_response = mock.MagicMock()
        mocked_response.json.return_value = GEOJSON_SAMPLE
        mocked_post.return_value = mocked_response
        dummy = Dummy()
        dummy.terralego_geometry = 'POINT(-104.590948 38.319914)'
        dummy.terralego_tags = json.dumps(['test', 'django_terralego.Dummy'])
        dummy.save()
        self.assertEqual(mocked_post.call_count, 1)
        tags = mocked_post.mock_calls[0][2]['data']['tags']
        self.assertEqual(tags, json.dumps(['django_terralego.Dummy', 'test']))

    @mock.patch('requests.get')
    def test_closest_with_right_tag(self, mocked_get):
        mocked_response = mock.MagicMock()
        mocked_response.json.return_value = GEOJSON_SAMPLE
        mocked_get.return_value = mocked_response
        dummy = Dummy.objects.create(terralego_id=GEOJSON_SAMPLE['id'])
        dummy2 = Dummy.objects.create(terralego_id="123234fb-ec81-4189-ab6b-ac9b1483e123")
        entry = dummy2.closest()
        self.assertEqual(entry, dummy)
        self.assertEqual(mocked_get.call_count, 1)

    @mock.patch('requests.get')
    def test_closest_with_bad_tag(self, mocked_get):
        mocked_response = mock.MagicMock()
        return_value = deepcopy(GEOJSON_SAMPLE)
        return_value['properties']['tags'] = []
        mocked_response.json.return_value = return_value
        mocked_get.return_value = mocked_response
        dummy = Dummy.objects.create()
        entry = dummy.closest()
        self.assertIsInstance(entry, dict)
        self.assertDictEqual(entry, return_value)
        self.assertEqual(mocked_get.call_count, 1)
