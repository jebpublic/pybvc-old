"""
vrouter5600.py: vRouter-5600 specific properties and communication methods


"""

import string
import json

from pybvc.controller.netconfnode import NetconfNode
from pybvc.common.status import OperStatus, STATUS
from pybvc.common.utils import remove_empty_from_dict


#===============================================================================
# Class 'VRouter5600'
#===============================================================================
class VRouter5600(NetconfNode):
    """Class that represents an instance of vRouter-5600 (NETCONF capable server device)."""
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, ctrl, name, ipAddr, portNum, adminName, adminPassword, tcpOnly=False):
        """Initializes this object properties."""
        super(VRouter5600, self).__init__(ctrl, name, ipAddr, portNum, adminName, adminPassword, tcpOnly)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        """Returns string representation of this object."""
        return str(vars(self))

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        """Returns JSON representation of this object."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_schemas(self):
        ctrl = self.ctrl
        myname = self.name
        return ctrl.get_schemas(myname)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_schema(self, schemaId, schemaVersion):
        ctrl = self.ctrl
        myname = self.name
        return ctrl.get_schema(myname, schemaId, schemaVersion)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_cfg(self):        
        status = OperStatus()
        cfg = None
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)

        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            cfg = resp.content
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, cfg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_firewalls_cfg(self):        
        status = OperStatus()
        cfg = None
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall"        
        modelref = templateModelRef       
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        url += modelref
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            cfg = resp.content
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, cfg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_firewall_instance_cfg(self, instance):        
        status = OperStatus()
        cfg = None
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall/name/{}"     
        modelref = templateModelRef.format(instance)
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        url += modelref
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            cfg = resp.content
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)

        return (status, cfg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def create_firewall_instance(self, fwInstance):        
        status = OperStatus()
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        headers = {'content-type': 'application/yang.data+json'}
        payload = fwInstance.get_payload()
        
        resp = ctrl.http_post_request(url, payload, headers)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200 or resp.status_code == 204):
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, None)
    
    #---------------------------------------------------------------------------
    # TBD
    #---------------------------------------------------------------------------
    def add_firewall_instance_rule(self, fwInstance, fwRule):
        pass
    
    #---------------------------------------------------------------------------
    # TBD
    #---------------------------------------------------------------------------
    def update_firewall_instance_rule(self, fwInstance, fwRule):
        pass
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def delete_firewall_instance(self, fwInstance):
        status = OperStatus()
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        ext = fwInstance.get_url_extension()
        url += ext
        rules = fwInstance.get_rules()
        p1 = "/name/"
        url += p1
        for item in rules:
            name = item.get_name()
            resp = ctrl.http_delete_request(url + name, data=None, headers=None)
            if(resp == None):
                status.set_status(STATUS.CONN_ERROR)
                break
            elif(resp.content == None):
                status.set_status(STATUS.CTRL_INTERNAL_ERROR)
                break
            elif (resp.status_code == 200):
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.HTTP_ERROR, resp)
                break
            
        return (status, None)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_dataplane_interface_firewall(self, ifName,
                                         inboundFwName, outboundFwName):
        status = OperStatus()
        ctrl = self.ctrl
        headers = {'content-type': 'application/yang.data+json'}
        url = ctrl.get_ext_mount_config_url(self.name)        
        obj = DataplaneInterfaceFirewall(ifName)
        
        if (inboundFwName != None):
            obj.add_in_item(inboundFwName)
        
        if (outboundFwName != None):
            obj.add_out_item(outboundFwName)
        
        payload = obj.get_payload()
        urlext = obj.get_url_extension()
        
        resp = ctrl.http_put_request(url + urlext, payload, headers)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, None)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def delete_dataplane_interface_firewall(self, ifName):        
        status = OperStatus()
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/{}/vyatta-security-firewall:firewall/"
        modelref = templateModelRef.format(ifName)
        myname = self.name
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(myname)  
        
        resp = ctrl.http_delete_request(url + modelref, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)

        return (status, None)
    
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_interfaces_list(self):
        ifList = []
        
        result = self.get_interfaces_cfg()
        status = result[0]
        if(status.eq(STATUS.OK)):
            cfg = result[1]
            p1 = 'interfaces'
            if(p1 in cfg):
                d = json.loads(cfg).get(p1)
                p2 = 'tagnode'
                for k, v in d.items():
                    print k
                    print type(v)
                    if (isinstance(v, list)):
                        for item in v:
                            if p2 in item:
                                ifList.append(item[p2])
        
        return (status, ifList)
    
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_interfaces_cfg(self):        
        status = OperStatus()
        cfg = None
        templateModelRef = "vyatta-interfaces:interfaces"        
        modelref = templateModelRef       
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(self.name)
        url += modelref        
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            cfg = resp.content
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, cfg)
    
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_dataplane_interfaces_list(self):        
        dpIfList = []

        result = self.get_interfaces_cfg()
        status = result[0]
        if(status.eq(STATUS.OK)):
            cfg = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-dataplane:dataplane'
            if(p1 in cfg and p2 in cfg):
                items = json.loads(cfg).get(p1).get(p2)
                p3 = 'tagnode'
                for item in items:
                    if p3 in item:
                        dpIfList.append(item[p3])
        
        return (status, dpIfList)
    

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_dataplane_interfaces_cfg(self):
        dpIfCfg = None
        
        result = self.get_interfaces_cfg()
        status = result[0]
        if(status.eq(STATUS.OK)):
            cfg = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-dataplane:dataplane'
            if(p1 in cfg and p2 in cfg):
                dpIfCfg = json.loads(cfg).get(p1).get(p2)

        return (status, dpIfCfg)
    

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_dataplane_interface_cfg(self, ifName):        
        status = OperStatus()
        cfg = None
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/{}"
        modelref = templateModelRef.format(ifName)
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(self.name)
        url += modelref

        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            cfg = resp.content
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, cfg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_loopback_interfaces_list(self):
        lbInterfaces = []
        
        result = self.get_interfaces_cfg()
        status = result[0]
        if(status.eq(STATUS.OK)):
            cfg = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-loopback:loopback'
            if(p1 in cfg and p2 in cfg):
                items = json.loads(cfg).get(p1).get(p2)
                p3 = 'tagnode'
                for item in items:
                    if p3 in item:
                        lbInterfaces.append(item[p3])
      
        return (status, lbInterfaces)        
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_loopback_interfaces_cfg(self):
        lbIfCfg = None

        result = self.get_interfaces_cfg()
        status = result[0]
        if(status.eq(STATUS.OK)):
            cfg = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-loopback:loopback'
            if(p1 in cfg and p2 in cfg):
                lbIfCfg = json.loads(cfg).get(p1).get(p2)
        
        return (status, lbIfCfg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_loopback_interface_cfg(self, ifName):        
        status = OperStatus()
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-loopback:loopback/{}"
        modelref = templateModelRef.format(ifName)
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(self.name)
        url += modelref

        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, resp)

#===============================================================================
# Class 'Firewall'
#===============================================================================
class Firewall():
    mn1 = "vyatta-security:security"
    mn2 = "vyatta-security-firewall:firewall"
    def __init__(self):
        self.name = []
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        return str(vars(self))
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 
    
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_payload(self):
        s = self.to_json()
        s = string.replace(s, 'typename', 'type-name')
        d1 = json.loads(s)
        d2 = remove_empty_from_dict(d1)
        payload = {self.mn1:{self.mn2:d2}}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_url_extension(self):
        return (self.mn1 + "/" +  self.mn2)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_rules(self, rules):
        self.name.append(rules)
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_rules(self):
        rules = []
        for item in self.name:
            rules.append(item)
        return rules

#===============================================================================
# Class 'Rules'
#===============================================================================
class Rules():
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, name):
        self.tagnode = name
        self.rule = []
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        return str(vars(self))
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_rule(self, rule):
        self.rule.append(rule)
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_name(self):
        return self.tagnode 

#===============================================================================
# Class 'Rule'
#===============================================================================
class Rule():
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, number):
        self.tagnode = number
        self.source = Object()
        self.icmp = Object()
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        return str(vars(self))
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_action(self, action):
        self.action = action
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_source_address(self, srcAddr):
        self.source.address = srcAddr

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_icmp_typename(self, typeName):
        self.protocol = "icmp"
        self.icmp.typename = typeName


#===============================================================================
# Class 'DataplaneInterfaceFirewall'
#===============================================================================
class DataplaneInterfaceFirewall():
    mn1 = "vyatta-interfaces:interfaces"
    mn2 = "vyatta-interfaces-dataplane:dataplane"
    mn3 = "vyatta-security-firewall:firewall"

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, ifName):
        self.tagnode = ifName
        self.firewall = Object()
        self.firewall.inlist = []
        self.firewall.outlist = []
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_in_item(self, name):
        self.firewall.inlist.append(name)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_out_item(self, name):
        self.firewall.outlist.append(name)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_url_extension(self):
        return (self.mn1 + "/" + self.mn2 + "/" +  self.tagnode)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_name(self):
        return self.tagnode
     
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_payload(self):        
        s = self.to_json()
        s = string.replace(s, 'firewall', self.mn3)
        s = string.replace(s, 'inlist', "in")
        s = string.replace(s, 'outlist', "out")
        obj = json.loads(s)
        payload = {self.mn2:obj}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)

#===============================================================================
# Class 'Object'
#===============================================================================
class Object():
    pass
        
