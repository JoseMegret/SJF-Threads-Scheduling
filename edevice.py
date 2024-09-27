#=================================================================================
#
# Programmer : Jose A. Megret    CCOM 4017 Section 0U1
# Stu.Num : 801-21-7986          First Semester 2024-2025
# Assignment 02                  Prof. Jose Ortiz Ubarri
# File : edevice.py              Fecha: September 27 2024
#
#=================================================================================
import socket
import random
import time
import psutil 

# Function to get the list of processes running on the system using psutil
def get_processes():
    processes = []
    for proc in psutil.process_iter(['name']):
        try:
            processes.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

# Function to simulate sending process CPU times to the cluster
def send_process_times(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_address, server_port))
        print(f"Connected to cluster at {server_address}:{server_port}")
        
        processes = get_processes()
        for process in processes[:5]:  # Limiting to 5 processes for simplicity
            cpu_time = random.randint(1, 5)  # Random CPU time between 1 to 5 seconds
            message = f"{process}:{cpu_time}"
            client_socket.sendall(message.encode('utf-8'))
            print(f"Sent: {message}")
            time.sleep(random.randint(1, 5))  # Sleep between 1 to 5 seconds
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python edevice.py <server address> <server port>")
        sys.exit(1)
    
    server_address = sys.argv[1]  
    server_port = int(sys.argv[2])  
    
    send_process_times(server_address, server_port)
