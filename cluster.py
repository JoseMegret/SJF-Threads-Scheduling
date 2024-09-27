#=================================================================================
#
# Programmer : Jose A. Megret    CCOM 4017 Section 0U1
#                                First Semester 2024-2025
# Assignment 02                  Prof. Jose Ortiz Ubarri
# File : cluster.py              Date: September 27 2024
#
#=================================================================================
import socket
import threading
import time
from threading import Semaphore, Lock

# Global variables
job_queue = []  # Shared queue for jobs
queue_lock = Lock()  # Mutex for protecting access to the job queue
queue_semaphore = Semaphore(0)  # Semaphore for blocking consumers until jobs arrive

# Function for the head node (producer thread) to receive jobs and sort by SJF
def head_node(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(5)
    print(f"Head node listening on port {server_port}")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            
            # Extract process name and CPU time
            process_name, cpu_time = data.split(':')
            cpu_time = int(cpu_time)
            
            # Critical region: Add job to queue and sort it by CPU time (SJF)
            with queue_lock:
                job_queue.append((process_name, cpu_time))
                job_queue.sort(key=lambda x: x[1])  # Sort by CPU time (SJF)
                print(f"Job added and sorted: {job_queue}")
            
            # Signal a consumer thread that a job is available
            queue_semaphore.release()
        
        conn.close()

# Function for the consumer threads to execute jobs
def consumer_thread(consumer_id):
    total_time = 0
    while True:
        # Wait until a job is available
        queue_semaphore.acquire()
        
        # Critical region: Extract job from queue
        with queue_lock:
            job = job_queue.pop(0)  # Get the first job (SJF guarantees it's the shortest)
            process_name, cpu_time = job
        
        # Simulate execution of the job
        print(f"Consumer {consumer_id} executing {process_name} for {cpu_time} seconds")
        time.sleep(cpu_time)
        
        total_time += cpu_time
        print(f"Consumer {consumer_id} total time: {total_time}")

# Main function to run the cluster
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cluster.py <server port>")
        sys.exit(1)
    
    server_port = int(sys.argv[1])
    
    # Start the head node (producer) thread
    head_thread = threading.Thread(target=head_node, args=(server_port,))
    head_thread.start()
    
    # Start two consumer threads
    consumer1 = threading.Thread(target=consumer_thread, args=(1,))
    consumer2 = threading.Thread(target=consumer_thread, args=(2,))
    consumer1.start()
    consumer2.start()
    
    head_thread.join()
    consumer1.join()
    consumer2.join()

