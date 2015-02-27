"""
netconfnode.py: Controller's NETCONF node specific properties


"""
import json

class NetconfNode(object):
    """Class that represents a NETCONF capable server device.
    
        :param controller: :class:`pybvc.controller.controller.Controller`
        :param string nodeName: The name of the node
        :param string ipAddr:  The ip address for the netconf device
        :param int portNum:  The port number to communicate NETCONF to the device
        :param string adminName:  The username to authenticate setup of the NETCONF communication 
        :param string adminPassword:  The password to authenticate setup of the NETCONF communication 
        :param boolean tcpOnly:  Use TCP only or not. 
        :return: The newly created NetconfNode instance.
        :rtype: :class:`pybvc.controller.netconfnode.NetconfNode`
    """
    
    def __init__(self, controller=None, nodeName=None, ipAddr=None, portNum=None,
                 adminName=None, adminPassword=None, tcpOnly=False):

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
