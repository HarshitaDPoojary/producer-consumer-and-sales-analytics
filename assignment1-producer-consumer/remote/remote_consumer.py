"""
Remote Consumer - Connects to queue server and consumes items

Usage:
    Terminal 3: python remote_consumer.py --host localhost --port 5555 --items 50 --name Consumer-1

This connects to the queue server and starts consuming items.
"""

import socket
import pickle
import argparse
import time
import sys


def main():
    parser = argparse.ArgumentParser(description='Connect as consumer to queue server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=5555, help='Server port (default: 5555)')
    parser.add_argument('--items', '-i', type=int, default=50, help='Number of items to consume (default: 50)')
    parser.add_argument('--name', '-n', default='Consumer-1', help='Consumer name (default: Consumer-1)')
    parser.add_argument('--delay', '-d', type=float, default=0.015, help='Delay between items in seconds (default: 0.015)')

    args = parser.parse_args()

    print("="*70)
    print(f"CONSUMER: {args.name}")
    print("="*70)
    print(f"Connecting to {args.host}:{args.port}...")

    try:
        # Connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((args.host, args.port))

        # Register as consumer
        register_msg = {'type': 'consumer', 'name': args.name}
        client_socket.send(pickle.dumps(register_msg))

        # Wait for registration acknowledgment
        ack = pickle.loads(client_socket.recv(1024))
        if ack['status'] != 'connected':
            print("Failed to register with server")
            sys.exit(1)

        print(f"Connected! Starting to consume {args.items} items...\n")

        items_consumed = 0
        consumed_items = []
        start_time = time.time()

        # Consume items
        for i in range(args.items):
            # Send GET command
            message = {'command': 'get'}
            client_socket.send(pickle.dumps(message))

            # Wait for item
            response = pickle.loads(client_socket.recv(1024))

            if response['status'] == 'ok':
                item = response.get('item')
                consumed_items.append(item)
                items_consumed += 1
                print(f"[{items_consumed}/{args.items}] Consumed: {item}")
            else:
                print(f"Error: {response.get('message', 'Unknown error')}")

            time.sleep(args.delay)

        # Send DONE command
        message = {'command': 'done'}
        client_socket.send(pickle.dumps(message))
        response = pickle.loads(client_socket.recv(1024))

        total_time = time.time() - start_time

        print("\n" + "="*70)
        print("CONSUMER FINISHED")
        print("="*70)
        print(f"Items consumed:  {items_consumed}")
        print(f"Time taken:      {total_time:.3f}s")
        print(f"Rate:            {items_consumed/total_time:.1f} items/sec")
        print("="*70)

        client_socket.close()

    except ConnectionRefusedError:
        print(f"\nError: Could not connect to server at {args.host}:{args.port}")
        print("Make sure the queue server is running first!")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
