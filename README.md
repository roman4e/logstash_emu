# logstash_emu
Logstash simplest emulator.
Run logstash_emu if your app requires it, but you need some lightweight emulation.

## installation

### generate keys
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"

## config
Configuration inside app file.

## running

python3 ./logstash-emu.py
