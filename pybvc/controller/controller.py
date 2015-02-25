"""
controller.py: Controller's properties and communication methods


"""

import json
import xmltodict
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, Timeout
from pybvc.common.status import OperStatus, STATUS


class Controller():
    """Class that represents a Controller device."""
    
    def __init__(self, ipAddr, portNum, adminName, adminPassword, timeout=5):
        """Initializes this object properties."""        
        self.ipAddr = ipAddr
        self.portNum = portNum
        self.adminName = adminName
        self.adminPassword = adminPassword
        self.timeout = timeout
#        self.nodes = []
    '''
    def add_node(self,node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes
    
    def get_node(self, nodeName):
        node = None
        for item in self.nodes:
            if(isinstance(item, NetconfNode) and item.name == nodeName):
                node = item
                break
        return node
    '''
    
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
    def http_get_request(self, url, data, headers):
        """Sends HTTP GET request to a remote server and returns the response."""
        resp = None
        
        try:
            resp = requests.get(url,
                                auth=HTTPBasicAuth(self.adminName, self.adminPassword), 
                                data=data, headers=headers, timeout=self.timeout)
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)
        
        return (resp)
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def http_post_request(self, url, data, headers):
        """Sends HTTP POST request to a remote server and returns the response."""
        resp = None
        
        try:
            resp = requests.post(url,
                                 auth=HTTPBasicAuth(self.adminName, self.adminPassword),
                                 data=data, headers=headers, timeout=self.timeout)
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)

        return (resp)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def http_put_request(self, url, data, headers):
        """Sends HTTP PUT request to a remote server and returns the response."""
        resp = None

        try:
            resp = requests.put(url,
                                auth=HTTPBasicAuth(self.adminName, self.adminPassword),
                                data=data, headers=headers, timeout=self.timeout)
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)
        
        return (resp)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def http_delete_request(self, url, data, headers):
        """Sends HTTP DELETE request to a remote server and returns the response."""
        resp = None
        
        try:
            resp = requests.delete(url,
                                   auth=HTTPBasicAuth(self.adminName, self.adminPassword),
                                   data=data, headers=headers, timeout=self.timeout)
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)

        return (resp)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def check_node_config_status(self, nodeId):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)

        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            status.set_status(STATUS.NODE_CONFIGURED)
        else:
            status.set_status(STATUS.DATA_NOT_FOUND, resp)
        
        return (status, None)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def check_node_conn_status(self, nodeId):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
        
        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            found = False
            connected = False
            p1 = 'nodes'
            p2 = 'node'
            if(p1 in resp.content and p2 in resp.content):            
                itemlist = json.loads(resp.content).get(p1).get(p2)            
                for item in itemlist:
                    p3 = 'id'
                    if(p3 in item and item[p3] == nodeId):
                        found = True
                        p4 = 'netconf-node-inventory:connected'
                        if (p4 in item and item[p4] == True):
                            connected = True
                        break
            if(connected):
                status.set_status(STATUS.NODE_CONNECTED)
            elif(found):
                status.set_status(STATUS.NODE_DISONNECTED)
            else:
                status.set_status(STATUS.NODE_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
                
        return (status, None)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_all_nodes_in_config(self):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)        
        nlist = [] 
        
        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'nodes'
            p2 = 'node'
            if(p1 in resp.content and p2 in resp.content):
                elemlist = json.loads(resp.content).get(p1).get(p2)
                for elem in elemlist:
                    p3 = 'id'
                    if(p3 in elem):
                        nlist.append(str(elem[p3]))
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, nlist)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_all_nodes_conn_status(self):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
        nlist = [] 

        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'nodes'
            p2 = 'node'
            if(p1 in resp.content and p2 in resp.content):            
                status.set_status(STATUS.OK)
                itemlist = json.loads(resp.content).get(p1).get(p2)
                for item in itemlist:
                    p3 = 'id'
                    if (p3 in item):
                        nd = dict()
                        nd.update({p2 : item[p3]})
                        p4 = 'netconf-node-inventory:connected'
                        p5 = 'connected'
                        if ((p4 in item) and (item[p4] == True)):
                            nd.update({p5 : True})
                        else:
                            nd.update({p5 : False})
                        nlist.append(nd)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)

        return (status, nlist)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_schemas(self, nodeName):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:netconf-state/schemas"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName)
        slist = None
        
        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'schemas'
            p2 = 'schema'
            if(p1 in resp.content and p2 in resp.content):            
                status = OperStatus(STATUS.OK)
                data = json.loads(resp.content).get(p1).get(p2)
                slist = data
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, slist)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_schema(self, nodeName, schemaId, schemaVersion):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operations/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:get-schema"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName) 
        headers = {'content-type': 'application/yang.data+json', 'accept': 'text/json, text/html, application/xml, */*'}
        payload = {'input': {'identifier' : schemaId, 'version' : schemaVersion, 'format' : 'yang'}}
        schema = None

        resp = self.http_post_request(url, json.dumps(payload), headers)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            if(resp.headers.get('content-type') == "application/xml"):
                doc = xmltodict.parse(resp.content)
                try:
                    p1 = 'get-schema'
                    p2 = 'output'
                    p3 = 'data'
                    schema = doc[p1][p2][p3]
                    status.set_status(STATUS.OK)
                except (KeyError, TypeError, ValueError) as e:
                    print repr(e)
                    status.set_status(STATUS.DATA_NOT_FOUND)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
                print "TBD: not implemented content type parser"
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, schema)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_netconf_operations(self, nodeName):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operations/opendaylight-inventory:nodes/node/{}/yang-ext:mount/"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName) 
        olist = None

        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'operations'
            if(p1 in resp.content):
                olist = json.loads(resp.content).get(p1)
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND, resp)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, olist)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_all_modules_operational_state(self):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules"
        url = templateUrl.format(self.ipAddr, self.portNum)
        mlist = None

        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            try:
                p1 = 'modules'
                p2 = 'module'
                mlist = json.loads(resp.content).get(p1).get(p2)
                status.set_status(STATUS.OK)
            except (KeyError, TypeError, ValueError)as  e:
                print repr(e)
                status.set_status(STATUS.DATA_NOT_FOUND)
                
                
            '''
            p1 = 'modules'
            p2 = 'module'
            if(p1 in resp.content and p2 in resp.content):
                mlist = json.loads(resp.content).get(p1).get(p2)
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
            '''
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)

        return (status, mlist)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_module_operational_state(self, moduleType, moduleName):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules/module/{}/{}"              
        url = templateUrl.format(self.ipAddr, self.portNum, moduleType, moduleName)         
        module = None

        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'module'
            if(p1 in resp.content):
                module = json.loads(resp.content).get(p1)
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, module)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_sessions_info(self, nodeName):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:netconf-state/sessions"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName)
        slist = None
        
        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'sessions'
            if(p1 in resp.content):
                slist = json.loads(resp.content).get(p1)
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)                
        
        return (status, slist)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_streams_info(self):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/streams"        
        url = templateUrl.format(self.ipAddr, self.portNum)
        slist = None
        
        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'streams'
            if(p1 in resp.content):
                slist = json.loads(resp.content).get(p1)
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)                
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)

        return (status, slist)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_service_providers_info(self):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:services"        
        url = templateUrl.format(self.ipAddr, self.portNum)
        slist = None
        
        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'services'
            p2 = 'service'
            if(p1 in resp.content and p2 in resp.content):
                slist = json.loads(resp.content).get(p1).get(p2)
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)

        return (status, slist)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_service_provider_info(self, name):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:services/service/{}"
        url = templateUrl.format(self.ipAddr, self.portNum, name)         
        service = None
        
        resp = self.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            p1 = 'service'
            if(p1 in resp.content):
                service = json.loads(resp.content).get(p1)
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)                          
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)        
        
        return (status, service)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_netconf_node(self, node):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules"        
        xmlPayloadTemplate = '''
        <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
          <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
          <name>{}</name>
          <address xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</address>
          <port xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</port>
          <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</username>
          <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</password>
          <tcp-only xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</tcp-only>
          <event-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
            <name>global-event-executor</name>
          </event-executor>
          <binding-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
            <name>binding-osgi-broker</name>
          </binding-registry>
          <dom-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
            <name>dom-broker</name>
          </dom-registry>
          <client-dispatcher xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
            <name>global-netconf-dispatcher</name>
          </client-dispatcher>
          <processing-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">prefix:threadpool</type>
            <name>global-netconf-processing-executor</name>
          </processing-executor>
        </module>
        '''
        payload = xmlPayloadTemplate.format(node.name, node.ipAddr, node.portNum, node.adminName, node.adminPassword, node.tcpOnly)
        url = templateUrl.format(self.ipAddr, self.portNum)
        headers = {'content-type': 'application/xml', 'accept': 'application/xml'}
        
        resp = self.http_post_request(url, payload, headers)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200 or resp.status_code == 204):
            status.set_status(STATUS.OK)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, resp)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def delete_netconf_node(self, netconfdev):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/{}"
        url = templateUrl.format(self.ipAddr, self.portNum, netconfdev.name)

        resp = self.http_delete_request(url, data=None, headers=None)
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
    # TBD: 
    # NOTE: It is unclear which NETCONF node attributes are allowed for dynamic
    #       configuration changes. For now just follow an example that is
    #       published on ODL wiki:
    #       https://wiki.opendaylight.org/view/OpenDaylight_Controller:Config:Examples:Netconf
    #---------------------------------------------------------------------------
    def modify_netconf_node_in_config(self, netconfdev):
        status = OperStatus()
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules"      
        url = templateUrl.format(self.ipAddr, self.portNum)
        xmlPayloadTemplate = '''
        <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
          <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
          <name>{}</name>
          <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</username>
          <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</password>
        </module>
        '''
        payload = xmlPayloadTemplate.format(netconfdev.devName, netconfdev.adminName, netconfdev.adminPassword)
        headers = {'content-type': 'application/xml', 'accept': 'application/xml'}
        
        resp = self.http_post_request(url, payload, headers)
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
    def get_ext_mount_config_url(self, node):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/{}/yang-ext:mount/"
        url = templateUrl.format(self.ipAddr, self.portNum, node)
        return url    

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_ext_mount_operational_url(self, node):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/{}/yang-ext:mount/"
        url = templateUrl.format(self.ipAddr, self.portNum, node)
        return url    
