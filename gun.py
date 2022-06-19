bind = '{}:{}'.format('127.0.0.1', 5000)
max_request = 1000
backlog = 2048
timeout = 600
workers = 4
worker_class = 'sync'
daemon = False
debug = True
