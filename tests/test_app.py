"""HTTP behavior tests. Run from the project root with unittest discovery."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from app import app


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.previous_testing = app.testing
        app.testing = True
        self.addCleanup(setattr, app, 'testing', self.previous_testing)
        self.client = app.test_client()
        self.content = json.loads(
            (Path(__file__).resolve().parents[1] / 'content.json').read_text()
        )

    def test_home_renders_profile_and_all_projects(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/html')
        from markupsafe import escape
        html = response.get_data(as_text=True)
        self.assertIn(str(escape(self.content['name'])), html)
        for project in self.content['projects']:
            with self.subTest(project=project['title']):
                self.assertIn(str(escape(project['title'])), html)
                self.assertIn(str(escape(project['status'])), html)
                if project['url']:
                    self.assertIn('href="' + str(escape(project['url'])) + '"', html)
        self.assertNotIn('href="None"', html)

    def test_profile_text_is_html_escaped(self):
        self.content['bio'] = '<script>alert("example")</script>'
        with patch('app.Path.read_text', return_value=json.dumps(self.content)):
            html = self.client.get('/').get_data(as_text=True)
        self.assertNotIn('<script>alert(', html)
        self.assertIn('&lt;script&gt;', html)

    def test_stylesheet_is_served(self):
        response = self.client.get('/static/style.css')
        self.addCleanup(response.close)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/css')
        self.assertTrue(response.data)

    def test_health_response(self):
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual(response.get_json(), {'status': 'ok'})

    def test_health_does_not_depend_on_portfolio_content(self):
        with patch('app.Path.read_text', side_effect=OSError('Unavailable')):
            self.assertEqual(self.client.get('/healthz').status_code, 200)

    def test_unknown_page_returns_404(self):
        self.assertEqual(self.client.get('/does-not-exist').status_code, 404)

    def test_read_only_routes_reject_post(self):
        for route in ('/', '/healthz'):
            with self.subTest(route=route):
                self.assertEqual(self.client.post(route).status_code, 405)


if __name__ == '__main__':
    unittest.main()
