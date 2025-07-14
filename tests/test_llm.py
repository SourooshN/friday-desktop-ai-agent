import sys
import types
import unittest
from unittest.mock import patch, Mock

# Provide a minimal requests module if it's missing
if 'requests' not in sys.modules:
    requests_stub = types.ModuleType('requests')
    requests_stub.post = lambda *args, **kwargs: None
    sys.modules['requests'] = requests_stub

from core.llm.llm_interface import query_model


class QueryModelTests(unittest.TestCase):
    @patch('core.llm.llm_interface.requests.post')
    def test_query_model_returns_completion_text(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"completion": "hello world"}
        mock_post.return_value = mock_response

        result = query_model("foo", "bar")
        self.assertEqual(result, "hello world")
        mock_post.assert_called_once()


if __name__ == "__main__":
     unittest.main()
     