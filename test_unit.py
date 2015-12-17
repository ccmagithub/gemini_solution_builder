import unittest
import mock
from gemini_solution_builder.actions.list import ListSolution


class ActionListTest(unittest.TestCase):
    @mock.patch('gemini_solution_builder.actions.list.requests')
    @mock.patch('gemini_solution_builder.actions.list.json')
    def test_run(self, mock_json, mock_requests):
        solution = ListSolution(username='user', password='pass',
                                api_url='url_test')
        mock_json.loads.return_value = {'id': '1', 'name': 'test_name'}
        solution.run()
        mock_requests.get.assert_called_width('url_test')

if __name__ == '__main__':
    unittest.main()
