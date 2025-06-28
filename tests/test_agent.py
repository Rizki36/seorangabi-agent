import unittest
from agent_query import AgentQuery

class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = AgentQuery()

    def test_process_message(self):
        self.agent.start_chat("Hello!")
        response = self.agent.process_message("What can you do?")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")

if __name__ == '__main__':
    unittest.main()