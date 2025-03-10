from data.base_entity import BaseEntity

class Project(BaseEntity):
    def __init__(self, project_name, project_customer, project_status, project_id=None):
        self.project_customer = project_customer
        self.project_name = project_name
        self.project_status = project_status
        if project_id:
            self.project_id = project_id

    def is_valid(self):
        if len(self.project_customer) > 3:
            if self.project_name != any(char.isdigit() for char in self.project_name):
                if "project" not in self.project_name.lower():
                    return True
        return False

    def display(self):
        return f"Project: {self.name}, Customer: {self.project_customer}, Status: {self.status}"

