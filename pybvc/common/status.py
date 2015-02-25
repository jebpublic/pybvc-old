"""
status.py: Operational Status of a performed HTTP communication session


"""

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

#
# Status codes to be set in result of HTTP communication session
#
STATUS = enum('OK', 'CONN_ERROR',
              'DATA_NOT_FOUND', 'BAD_REQUEST',
              'UNAUTHORIZED_ACCESS', 'INTERNAL_ERROR',
              'NODE_CONNECTED', 'NODE_DISONNECTED',
              'NODE_NOT_FOUND', 'NODE_CONFIGURED',                   
              'HTTP_ERROR', 'UNKNOWN')

class OperStatus(object):
    """Operational status of completed HTTP session"""
    """and methods for easy parsing of the status data."""
    def __init__(self, status_code=None, http_resp=None):
        """Initializes this object properties."""
        self.status_code = status_code
        self.http_resp = http_resp
    
    def set_status(self, status_code, http_resp=None):
        self.status_code = status_code
        self.http_resp=http_resp
    
    def to_string(self):
        return self.__status_code_string()
    
    def brief(self):
        return self.__status_code_string()
    
    def detail(self):
        if(self.http_resp != None and self.http_resp.content != None):
            return self.http_resp.content
        else:
            return ""
    
    def code(self):
        return self.status_code
    
    def eq(self, status_code):
        if(self.status_code == status_code):
            return True
        else:
            return False
    
    def __status_code_string(self):
        if (self.status_code == STATUS.OK):
            return "Success"
        elif( self.status_code == STATUS.CONN_ERROR):
            return "Server connection error"
        elif( self.status_code == STATUS.DATA_NOT_FOUND):
            return "Requested data not found"
        elif( self.status_code == STATUS.BAD_REQUEST):
            return "Bad or invalid data in request"
        elif( self.status_code == STATUS.UNAUTHORIZED_ACCESS):
            return "Server unauthorized access"
        elif( self.status_code == STATUS.INTERNAL_ERROR):
            return "Internal Server Error"        
        elif( self.status_code == STATUS.NODE_CONNECTED):
            return "Node is connected"
        elif( self.status_code == STATUS.NODE_DISONNECTED):
            return "Node is disconnected"
        elif( self.status_code == STATUS.NODE_NOT_FOUND):
            return "Node not found"
        elif( self.status_code == STATUS.NODE_CONFIGURED):
            return "Node is configured"
        elif( self.status_code == STATUS.HTTP_ERROR):
            errMsg = "HTTP error"
            if(self.http_resp != None and 
               self.http_resp.status_code and
               self.http_resp.reason != None):
                errMsg += " %d - '%s'" % (self.http_resp.status_code, self.http_resp.reason)
            return errMsg
        elif( self.status_code == STATUS.UNKNOWN):
            return "Unknown error"
        else:
            print ("Error: undefined status code %s" % self.status_code)
            raise ValueError('!!!undefined status code')
