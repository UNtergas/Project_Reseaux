import os

PIPE_NAME = '/tmp/my_pipe'

if not os.path.exists(PIPE_NAME):
    os.mkfifo(PIPE_NAME)

with open(PIPE_NAME, 'w') as f:
    f.write('Hello from Python!')