# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - present bcstechnologies.com
"""

from api import app, db
from api.scheduler import start_scheduler

@app.shell_context_processor
def make_shell_context():
    return {"app": app,
            "db": db
            }

if __name__ == '__main__':
    # Upadted the path of the SSL certificates for server configurations
    start_scheduler()
    context = ( '/etc/letsencrypt/live/leadconnectai.in/fullchain.pem' , '/etc/letsencrypt/live/leadconnectai.in/privkey.pem')
    app.run(debug=True, host="leadconnectai.in", port=443, ssl_context=context)
