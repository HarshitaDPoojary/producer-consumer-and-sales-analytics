"""
Remote Producer - Connects to queue server and produces items

Usage:
    Terminal 2: python remote_producer.py --host localhost --port 5555 --items 50 --name Producer-1

This connects to the queue server and starts producing items.
"""

import socket
import pickle
import argparse
import time
import sys

def main():
    parser = argparse.ArgumentParser(description='Connect as producer to queue server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=5555, help='Server port (default: 5555)')
    parser.add_argument('--items', '-i', type=int, default=50, help='Number of items to produce (default: 50)')
    parser.add_argument('--name', '-n', default='Producer-1', help='Producer name (default: Producer-1)')
    parser.add_argument('--delay', '-d', type=float, default=0.01, help='Delay between items in seconds (default: 0.01)')

    args = parser.parse_args()

    print("="*70)
    print(f"PRODUCER: {args.name}")
    print("="*70)
    print(f"Connecting to {args.host}:{args.port}...")

    try:
        # Connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((args.host, args.port))

        # Register as producer
        register_msg = {'type': 'producer', 'name': args.name}
        client_socket.send(pickle.dumps(register_msg))

        print(f"Connected! Starting to produce {args.items} items...\n")

        items_produced = 0
        start_time = time.time()

        # Produce items
        for i in range(args.items):
            item = f"{args.name}-Item-{i}"

            # Send PUT command
            message = {'command': 'put', 'item': item}
            client_socket.send(pickle.dumps(message))

            # Wait for acknowledgment
            response = pickle.loads(client_socket.recv(1024))

            if response['status'] == 'ok':
                items_produced += 1
                print(f"[{items_produced}/{args.items}] Produced: {item}")
            else:
                print(f"Error: {response.get('message', 'Unknown error')}")

            time.sleep(args.delay)

        # Send DONE command
        message = {'command': 'done'}
        client_socket.send(pickle.dumps(message))
        response = pickle.loads(client_socket.recv(1024))

        total_time = time.time() - start_time

        print("\n" + "="*70)
        print("PRODUCER FINISHED")
        print("="*70)
        print(f"Items produced:  {items_produced}")
        print(f"Time taken:      {total_time:.3f}s")
        print(f"Rate:            {items_produced/total_time:.1f} items/sec")
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
