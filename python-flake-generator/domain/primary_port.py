from port import Port

class PrimaryPort(Port):

    def priority(self) -> int:
        """Must be implemented by subclasses"""
        raise NotImplementedError("priority() must be implemented by subclasses")

    def accept(self, app):
        """Must be implemented by subclasses"""
        raise NotImplementedError("accept() must be implemented by subclasses")
