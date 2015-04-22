#!env python
from __future__ import print_function
from flask import Flask

import json
import os
import sys

lifecycle = None
creds = None
if 'VCAP_SERVICES' in os.environ: 
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    lifecycle = vcap_services.get('lifecycle-sb') 
    if lifecycle is not None:
        creds = lifecycle.get('credentials') 
    if creds is not None:
        user = creds.get('username')
        password = creds.get('password') 
        uri = cres.get('uri') 
else:
    print ("VCAP_SERVICES not found!!!", file=sys.stderr)

port = 8003
if 'PORT' in os.environ: 
    port = int(os.getenv("PORT"))

Flask.get = lambda self, path: self.route(path, methods=['get'])

app = Flask(__name__)

@app.get('/')
def get_root(): 
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
