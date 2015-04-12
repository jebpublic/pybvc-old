"""
openflownode.py: Controller's OpenFlow node specific properties


"""
import json

class OpenflowNode(object):
    """Class that represents a NETCONF capable server device."""
    
    def __init__(self, controller=None, nodeName=None):
        """Initializes this object properties."""
        self.ctrl = controller
        self.name = nodeName
    
    def to_string(self):
        """Returns string representation of this object."""
        return str(vars(self))

    def to_json(self):
        """Returns JSON representation of this object."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
