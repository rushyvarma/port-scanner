import asyncio
import socket
import sys
import time

usage = "python3 port_scan.py TARGET START_PORT END_PORT"

print("-"*70)
print("RUSH Port Scanner")
print("-"*70)

start_time = time.time()

if len(sys.argv) != 4:
    print(usage)
    sys.exit()

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Name resolution error")
    sys.exit()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

print("Scanning target:", target)

async def scan_port(port):
    try:
        reader, writer = await asyncio.open_connection(target, port)
        print(f"Port {port} is OPEN")
        writer.close()
    except Exception as e:
        pass

async def scan_range(start_port, end_port):
    tasks = []
    for port in range(start_port, end_port + 1):
        tasks.append(scan_port(port))
    await asyncio.gather(*tasks)

async def main():
    chunk_size = 100
    for i in range(start_port, end_port + 1, chunk_size):
        chunk_end = min(i + chunk_size - 1, end_port)
        await scan_range(i, chunk_end)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Scan interrupted by user.")

end_time = time.time()
print("Time Elapsed:", end_time - start_time, 's')
