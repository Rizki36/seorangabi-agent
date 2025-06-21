import unittest
from src.agent import Agent

class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent()

    def test_start_chat(self):
        response = self.agent.start_chat("Hello, how are you?")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")

    def test_process_message(self):
        self.agent.start_chat("Hello!")
        response = self.agent.process_message("What can you do?")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")

    def test_invalid_message(self):
        self.agent.start_chat("Hello!")
        response = self.agent.process_message("")
        self.assertEqual(response, "Invalid message.")

if __name__ == '__main__':
    unittest.main()