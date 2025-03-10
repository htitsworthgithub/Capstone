class BaseEntity:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def is_valid(self):
        return all([self.name, self.status])

    def display(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def contains_num(self):
        return any(char.isdigit() for char in self.name)