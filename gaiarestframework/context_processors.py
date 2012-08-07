import socket
try:
    HOSTNAME = socket.gethostname()
except Exception:
    HOSTNAME = 'localhost'

def hostname(context):
    return { 'HOSTNAME': HOSTNAME }