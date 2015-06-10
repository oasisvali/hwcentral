bind = "unix:devops/gunicorn.sock"
backlog = 64
workers = 3
# threads = 3   # use with python3 or by installing futures package into virtualenv
max_requests = 50
max_requests_jitter = 50
timeout = 30
graceful_timeout = 30
keepalive = 1
preload_app = True

accesslog = "devops/gunicorn_access.log"