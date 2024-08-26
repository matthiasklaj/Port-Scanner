import asyncio
import argparse
import socket

# Constants
TIMEOUT = 1  # Timeout for socket operations in seconds

async def scan_port(host, port, protocol):
    """Scan a single port on the given host asynchronously."""
    conn = asyncio.open_connection(host, port, ssl=False)
    try:
        if protocol == 'tcp':
            reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
            writer.close()
            await writer.wait_closed()
            return (port, 'TCP', 'Open')
        else:
            # For UDP, we use asyncio's datagram endpoint
            transport, protocol = await asyncio.wait_for(
                asyncio.get_event_loop().create_datagram_endpoint(
                    lambda: asyncio.DatagramProtocol(),
                    remote_addr=(host, port)
                ),
                timeout=TIMEOUT
            )
            transport.close()
            return (port, 'UDP', 'Open')
    except asyncio.TimeoutError:
        return (port, 'TCP' if protocol == 'tcp' else 'UDP', 'Closed')
    except Exception as e:
        return (port, 'TCP' if protocol == 'tcp' else 'UDP', f'Error: {str(e)}')

async def scan_ports(host, ports, protocol):
    """Scan a range of ports asynchronously on the given host."""
    tasks = [scan_port(host, port, protocol) for port in ports]
    return await asyncio.gather(*tasks)

def print_results(results):
    """Print the results of the port scan."""
    for port, protocol, status in results:
        print(f"Port {port} ({protocol}): {status}")

if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description='Network Port Scanner')
    parser.add_argument('host', type=str, help='Target host IP or hostname')
    parser.add_argument('ports', type=int, nargs='+', help='List of ports to scan')
    parser.add_argument('--protocol', choices=['tcp', 'udp'], default='tcp', help='Protocol to use (default: tcp)')

    args = parser.parse_args()

    # Scan ports
    print(f"Scanning {args.host} for {'TCP' if args.protocol == 'tcp' else 'UDP'} ports: {args.ports}")
    results = asyncio.run(scan_ports(args.host, args.ports, args.protocol))
    print_results(results)
