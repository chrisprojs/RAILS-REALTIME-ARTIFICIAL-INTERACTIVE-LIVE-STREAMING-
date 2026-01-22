from obswebsocket import obsws
# Konfigurasi koneksi WebSocket OBS
host = "localhost"
port = 4455  # Port in OBS WebSocket Server Settings
password = "socket"  # Password in OBS WebSocket Server Settings
ws = obsws(host, port, password)