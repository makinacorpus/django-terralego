from unittest import mock

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
            "test",
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
        dummy.geometry = 'POINT(-104.590948 38.319914)'
        dummy.save()
        self.assertEqual(dummy.terralego_id, GEOJSON_SAMPLE['id'])
        self.assertEqual(dummy.geometry, GEOJSON_SAMPLE['geometry'])
        self.assertEqual(dummy.tags, GEOJSON_SAMPLE['properties']['tags'])
        self.assertEqual(mocked_post.call_count, 1)

    @mock.patch('requests.get')
    def test_retrieve_geo_info(self, mocked_get):
        mocked_response = mock.MagicMock()
        mocked_response.json.return_value = GEOJSON_SAMPLE
        mocked_get.return_value = mocked_response
        dummy = Dummy(terralego_id=GEOJSON_SAMPLE['id'])
        self.assertEqual(dummy.geometry, GEOJSON_SAMPLE['geometry'])
        self.assertEqual(dummy.tags, GEOJSON_SAMPLE['properties']['tags'])
        self.assertEqual(mocked_get.call_count, 1)
