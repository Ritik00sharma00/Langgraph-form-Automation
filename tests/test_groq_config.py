import os
import unittest
from unittest.mock import patch

import app


class GroqConfigTest(unittest.TestCase):
    def test_default_model_is_gemma(self):
        self.assertEqual(app.GROQ_MODEL, "gemma2-9b-it")

    def test_missing_api_key_raises_runtime_error(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}, clear=True):
            with self.assertRaises(RuntimeError):
                app.get_groq_client()


if __name__ == "__main__":
    unittest.main()
