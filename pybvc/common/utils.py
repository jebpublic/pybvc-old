"""
utils.py: Helper utilities


"""
import sys
import time


def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.iteritems() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d

import yaml

def load_dict_from_file(f, d):
    try:
        with open(f, 'r') as f:
            obj = yaml.load(f)
        for k, v in obj.iteritems():
            d[k] = v
        return True
    except IOError:
        print("Error: failed to read file '%s'" % f)
        return False

def progress_wait_secs(msg=None, waitTime=None, sym="."):
    if (waitTime != None):
#        sys.stdout.write ("(waiting for %s seconds) " % waitTime)
#        sys.stdout.write ("waiting for %s seconds: " % waitTime)
#        sys.stdout.write ("waiting for %s seconds: " % waitTime)
        if (msg != None):
            sys.stdout.write ("%s" % msg)
        for i in range(0, waitTime, 1):
            print "%s" % sym, # <- no newline
            sys.stdout.flush() #<- makes python print it anyway
            time.sleep(1)
        sys.stdout.write ("\n")
