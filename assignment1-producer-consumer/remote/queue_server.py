"""
Queue Server - Central server hosting shared queue for remote producers/consumers

Usage:
    Terminal 1: python queue_server.py --queue-size 10 --port 5555

This starts a server that accepts connections from remote producers and consumers.
"""

import socket
import pickle
import threading
import argparse
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.shared_queue import SharedQueue


class QueueServer:
    """Server that hosts a shared queue and handles remote producer/consumer clients"""

    def __init__(self, host='localhost', port=5555, queue_size=10):
        self.host = host
        self.port = port
        self.queue = SharedQueue(max_size=queue_size)
        self.active_clients = []
        self.lock = threading.Lock()
        self.running = True

    def handle_client(self, client_socket, client_address):
        """Handle a connected client (producer or consumer)"""
        client_name = None
        client_type = None

        try:
            # Receive registration message
            data = client_socket.recv(1024)
            if not data:
                return

            register_msg = pickle.loads(data)
            client_type = register_msg.get('type', 'unknown')
            client_name = register_msg.get('name', f'{client_type}-{client_address[1]}')

            with self.lock:
                self.active_clients.append({
                    'name': client_name,
                    'type': client_type,
                    'address': client_address
                })

            print(f"[{time.strftime('%H:%M:%S')}] {client_name} ({client_type}) connected from {client_address}")

            # Handle client commands
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    message = pickle.loads(data)
                    command = message.get('command')

                    if command == 'put':
                        # Producer putting item
                        item = message.get('item')
                        self.queue.put(item)
                        response = {'status': 'ok'}
                        client_socket.send(pickle.dumps(response))

                    elif command == 'get':
                        # Consumer getting item
                        item = self.queue.get()
                        response = {'status': 'ok', 'item': item}
                        client_socket.send(pickle.dumps(response))

                    elif command == 'done':
                        # Client finished
                        response = {'status': 'ok'}
                        client_socket.send(pickle.dumps(response))
                        break

                    else:
                        response = {'status': 'error', 'message': 'Unknown command'}
                        client_socket.send(pickle.dumps(response))

                except Exception as e:
                    print(f"Error handling {client_name}: {e}")
                    break

        except Exception as e:
            print(f"Error with client {client_address}: {e}")

        finally:
            # Remove client from active list
            with self.lock:
                self.active_clients = [
                    c for c in self.active_clients
                    if c['name'] != client_name
                ]

            if client_name:
                print(f"[{time.strftime('%H:%M:%S')}] {client_name} disconnected")

            client_socket.close()

    def print_stats(self):
        """Print server statistics periodically"""
        while self.running:
            time.sleep(5)
            if not self.running:
                break

            with self.lock:
                producers = [c for c in self.active_clients if c['type'] == 'producer']
                consumers = [c for c in self.active_clients if c['type'] == 'consumer']

            metrics = self.queue.get_metrics()

            print("\n" + "="*70)
            print(f"[{time.strftime('%H:%M:%S')}] SERVER STATISTICS")
            print("="*70)
            print(f"Queue size:          {metrics['current_size']}/{self.queue.max_size}")
            print(f"Active producers:    {len(producers)}")
            print(f"Active consumers:    {len(consumers)}")
            print(f"Total puts:          {metrics['total_puts']}")
            print(f"Total gets:          {metrics['total_gets']}")
            print(f"Producer waits:      {metrics['producer_wait_count']}")
            print(f"Consumer waits:      {metrics['consumer_wait_count']}")
            print("="*70 + "\n")

    def start(self):
        """Start the server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            print("="*70)
            print("QUEUE SERVER STARTED")
            print("="*70)
            print(f"Host:        {self.host}")
            print(f"Port:        {self.port}")
            print(f"Queue size:  {self.queue.max_size}")
            print("="*70)
            print("\nWaiting for clients...\n")

            # Start statistics thread
            stats_thread = threading.Thread(target=self.print_stats, daemon=True)
            stats_thread.start()

            # Accept clients
            while self.running:
                try:
                    server_socket.settimeout(1.0)
                    try:
                        client_socket, client_address = server_socket.accept()
                        client_thread = threading.Thread(
                            target=self.handle_client,
                            args=(client_socket, client_address),
                            daemon=True
                        )
                        client_thread.start()
                    except socket.timeout:
                        continue

                except KeyboardInterrupt:
                    print("\n\nShutting down server...")
                    self.running = False
                    break

        except Exception as e:
            print(f"Server error: {e}")

        finally:
            server_socket.close()
            print("Server stopped.")


def main():
    parser = argparse.ArgumentParser(description='Start queue server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', '-p', type=int, default=5555, help='Server port (default: 5555)')
    parser.add_argument('--queue-size', '-q', type=int, default=10, help='Queue size (default: 10)')

    args = parser.parse_args()

    server = QueueServer(host=args.host, port=args.port, queue_size=args.queue_size)
    server.start()


if __name__ == "__main__":
    main()
