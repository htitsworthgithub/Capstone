from data.base_entity import BaseEntity

class Milestone(BaseEntity):
    def __init__(self, milestone_name, milestone_status):
        super().__init__(milestone_name, milestone_status)

    def to_dict(self):
        return {"milestone_name": self.name, "milestone_status": self.status}

    def out_string(self):
        return f"{self.name}: {self.status}"

    def display(self):
        return f"Milestone: {self.name}, Status: {self.status}"
    
    
    
class Milestones(BaseEntity):
    def __init__(self):
        self.milestones = []

    def add_milestone(self, milestone):
        self.milestones.append(milestone)

    def value(self):
        return self.milestones