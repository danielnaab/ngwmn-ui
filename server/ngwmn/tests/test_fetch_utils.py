"""
Unit tests for data fetch utility functions
"""

from unittest import TestCase, mock

import requests as r

from ..fetch_utils import generate_bounding_box_values, get_well_lithography


class TestGetWellLithography(TestCase):

    def setUp(self):
        self.test_service_root = 'http://fake.gov'
        self.test_agency_cd = 'DOOP'
        self.test_location_id = 'BP-1729'
        self.test_xml = '<site><agency>DOOP</agency><id>BP-1729</id></site>'

    @mock.patch('ngwmn.fetch_utils.r.get')
    def test_success(self, r_mock):
        m_resp = mock.Mock(r.Response)
        m_resp.content = self.test_xml
        m_resp.status_code = 200
        r_mock.return_value = m_resp
        result = get_well_lithography(self.test_service_root, self.test_agency_cd, self.test_location_id)
        self.assertEqual(result.tag, 'site')
        r_mock.assert_called_with(
            'http://fake.gov/ngwmn/iddata',
            params={'request': 'well_log', 'agency_cd': 'DOOP', 'siteNo': 'BP-1729'}
        )

    @mock.patch('ngwmn.fetch_utils.r.get')
    def test_service_failure(self, r_mock):
        m_resp = mock.Mock(r.Response)
        m_resp.status_code = 500
        r_mock.return_value = m_resp
        result = get_well_lithography(self.test_service_root, self.test_agency_cd, self.test_location_id)
        self.assertIsNone(result)

    @mock.patch('ngwmn.fetch_utils.r.get')
    def test_syntax_error(self, r_mock):
        m_resp = mock.Mock(r.Response)
        m_resp.content = 'Stuff'
        m_resp.status_code = 200
        r_mock.return_value = m_resp
        result = get_well_lithography(self.test_service_root, self.test_agency_cd, self.test_location_id)
        self.assertIsNone(result)


class TestGenerateBoundingBox(TestCase):

    def setUp(self):
        self.latitude = 45.48
        self.longitude = -16.71
        self.delta = 0.01

    def test_decimal_vals(self):
        result = generate_bounding_box_values(self.latitude, self.longitude, self.delta)
        self.assertAlmostEqual(result[0], -16.72)
        self.assertAlmostEqual(result[1], 45.47)
        self.assertAlmostEqual(result[2], -16.70)
        self.assertAlmostEqual(result[3], 45.49)

    def test_string_vals(self):
        result = generate_bounding_box_values(str(self.latitude), str(self.longitude), self.delta)
        self.assertAlmostEqual(result[0], -16.72)
        self.assertAlmostEqual(result[1], 45.47)
        self.assertAlmostEqual(result[2], -16.70)
        self.assertAlmostEqual(result[3], 45.49)
