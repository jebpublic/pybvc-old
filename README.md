# pybvc
Python framework to program your network via the Brocade Vyatta Controller 1.1.1 

## Installation:
```bash
pip install pybvc
```

## Documentation:
[Documentation](http://jebpublic.github.io/pybvc/)

## Applications using pybvc:
   - [pybvccmds](https://github.com/jebpublic/pybvccmds)
   - [pybvcsamples](https://github.com/jebpublic/pybvcsamples)

## Add and remove firewall on Vyatta vrouter5600 via BVC:

```python
import pybvc

from pybvc.netconfdev.vrouter.vrouter5600 import VRouter5600, Firewall, Rules, Rule
from pybvc.common.status import STATUS
from pybvc.controller.controller import Controller

print (">>> Create BVC controller instance")
ctrl = Controller("172.22.18.186", "8181" , 'admin' , 'admin') 

print (">>> Create Vyatta Router 5600 instance")
vrouter = VRouter5600(ctrl, "vRouter", "172.22.17.107", 830, "vyatta", "vyatta")


print (">>> Connect Vyatta Router 5600 to Brocade Vyatta Controller via NETCONF")
result = ctrl.add_netconf_node(vrouter)

print (">>> Define new firewall instance ACCEPT-SRC-IPADDR") 
firewall1 = Firewall()    
rules = Rules("ACCEPT-SRC-IPADDR")    
rule = Rule(30)
rule.add_action("accept")
rule.add_source_address("172.22.17.108")    
rules.add_rule(rule)
firewall1.add_rules(rules)


print (">>> Create ACCEPT-SRC-IPADDR on vrouter 5600") 
result = vrouter.create_firewall_instance(firewall1)


print (">>> Define new firewall instance DROP-ICMP") 
firewall2 = Firewall()    
rules = Rules("DROP-ICMP")    
rule = Rule(40)
rule.add_action("drop")
rule.add_icmp_typename("ping")
rules.add_rule(rule)
firewall2.add_rules(rules)   

print (">>> Create DROP-ICMP on vrouter 5600")  
result = vrouter.create_firewall_instance(firewall2)

print ("<<< Apply ACCEPT-SRC-IPADDR to inbound traffic and DROP-ICMP to outbound traffic on the dp0p1p7 dataplane interface" ) 
result = vrouter.set_dataplane_interface_firewall("dp0p1p7", "ACCEPT-SRC-IPADDR", "DROP-ICMP")

print (">>> Remove firewalls from dp0p1p7 dataplane interface")  
result = vrouter.delete_dataplane_interface_firewall("dp0p1p7")

print (">>> Remove firewall definitions from vrouter 5600")
result = vrouter.delete_firewall_instance(firewall1)
result = vrouter.delete_firewall_instance(firewall2)
```
