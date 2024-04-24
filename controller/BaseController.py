from abc import ABC, abstractmethod

class BaseController:

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_byID(self, id):
        pass

    @abstractmethod
    def create(self, data):
        pass
    
    @abstractmethod
    def update_byID(self, id, data):
        pass

    @abstractmethod
    def delete_byID(self, id):
        pass

    def handle_one_element(self, fullJson):
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson