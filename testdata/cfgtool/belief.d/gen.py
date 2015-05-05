#! /usr/bin/python

import json
from addict import Dict

d = Dict ()
d.db.db1.host = "db1_host"
d.db.db1.user = "db1_user"
d.db.db1.pw = "db1_pass"
d.db.db2.host = "db2_host"
d.db.db2.user = "db2_user"
d.db.db2.pw = "db2_pass"
d.db.db3.host = "db1_host"
d.db.db3.user = "db1_user"
d.db.db3.pw = "db1_pass"
d.var1 = "var1"
d.var2 = "var1"

print json.dumps (d, indent = 2)
