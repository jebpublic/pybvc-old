"""
netconfnode.py: Controller's NETCONF node specific properties


"""
import json

class NetconfNode(object):
    """Class that represents a NETCONF capable server device."""
    
    def __init__(self, controller=None, nodeName=None, ipAddr=None, portNum=None,
                 adminName=None, adminPassword=None, tcpOnly=False):
        """Initializes this object properties."""
        self.ctrl = controller
        self.name = nodeName
        self.ipAddr = ipAddr
        self.tcpOnly = tcpOnly
        self.portNum = portNum
        self.adminName = adminName
        self.adminPassword = adminPassword

    def to_string(self):
        """Returns string representation of this object."""
        return str(vars(self))

    def to_json(self):
        """Returns JSON representation of this object."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
