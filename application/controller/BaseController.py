from abc import ABC, abstractmethod

class BaseController:

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_byID(self, id):
        pass

    @abstractmethod
    def put_byID(self, id):
        pass

    @abstractmethod
    def update_byID(self, id):
        pass

    @abstractmethod
    def delete_byID(self, id):
        pass