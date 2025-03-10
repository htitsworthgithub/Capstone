import unittest
from data.project import Project

class TestProject(unittest.TestCase):
    def test_is_valid_with_valid_data(self):
        project = Project(project_name="NewApp", project_customer="CustomerA", project_status="Active")
        self.assertTrue(project.is_valid())

    def test_is_valid_with_short_customer_name(self):
        project = Project(project_name="NewApp", project_customer="Cus", project_status="Active")
        self.assertFalse(project.is_valid())

if __name__ == '__main__':
    unittest.main()