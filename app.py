import socketio

io = socketio.Server()
app = socketio.WSGIApp(io)

@io.event
def connect(sid, environ):
  print(sid, 'connected')

@io.event
def disconnect(sid):
  print(sid, 'disconnected')