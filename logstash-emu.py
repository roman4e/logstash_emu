import asyncio
import ssl
import json
import argparse

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[+] Connection from {addr}")
    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                log_event = json.loads(line.decode())
                print(json.dumps(log_event, indent=2))
            except json.JSONDecodeError:
                print(f"[!] Failed to decode JSON: {line.decode().strip()}")
    except Exception as e:
        print(f"[!] Error handling client {addr}: {e}")
    finally:
        print(f"[-] Connection from {addr} closed")
        writer.close()
        await writer.wait_closed()

async def main(host, port, use_tls, certfile, keyfile):
    ssl_context = None
    if use_tls:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        print("[+] TLS enabled")

    server = await asyncio.start_server(
        handle_client, host, port, ssl=ssl_context
    )

    addr = server.sockets[0].getsockname()
    print(f"[+] Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Logstash Emulator")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5044, help="Port to listen on")
    parser.add_argument("--tls", action="store_true", help="Enable TLS")
    parser.add_argument("--certfile", default="cert.pem", help="TLS certificate file")
    parser.add_argument("--keyfile", default="key.pem", help="TLS key file")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.host, args.port, args.tls, args.certfile, args.keyfile))
    except KeyboardInterrupt:
        print("\n[!] Server interrupted by user")
