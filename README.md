# SJF-Threads-Scheduling

### Embedded Device and Cluster with Shortest Job First (SJF) Scheduling
# Description

This project simulates a distributed system consisting of an embedded device and a central computer cluster, implementing a Shortest Job First (SJF) scheduling algorithm.

The embedded device generates computational jobs by retrieving the list of processes running on its system and assigns each process a random simulated CPU time. These jobs are then sent to the cluster for processing, where the head node receives them, places them in a queue, and sorts them based on the SJF algorithm (i.e., shortest CPU time first). Two consumer threads in the cluster then extract and "execute" the jobs by sleeping for the given CPU time.

The project showcases:

    Multithreading: Using threads to simulate concurrent operations on the cluster.
    Mutual exclusion and semaphores: Ensuring proper handling of shared resources between the producer and consumer threads.
    Inter-process communication: Using TCP sockets for communication between the embedded device and the cluster.

How to Use the Program
Prerequisites

    Python 3.x
    psutil library (if using the version with psutil):

    pip install psutil

Running the Embedded Device

    Open a terminal/command prompt.

    Navigate to the folder containing the project files.

    Run the embedded device with the following command:

    php

python edevice.py <server address> <server port>

    <server address>: The IP address of the machine where the cluster is running (e.g., 127.0.0.1 for localhost).
    <server port>: The port number on which the cluster is listening (should be less than 65,000).

Example:

bash

    python edevice.py 127.0.0.1 65432

    The embedded device will:
        Retrieve the list of running processes.
        Assign a random CPU time (1 to 5 seconds) to each process.
        Send these jobs to the cluster via TCP.
        Sleep randomly for 1 to 5 seconds between each job sent.

Running the Cluster

    Open another terminal/command prompt.

    Navigate to the folder containing the project files.

    Run the cluster with the following command:

    php

python cluster.py <server port>

    <server port>: The port number on which the cluster will listen for connections from the embedded device.

Example:

bash

    python cluster.py 65432

    The cluster will:
        Start the head node (producer thread) to accept jobs from the embedded device.
        Sort the jobs in the shared queue based on the SJF algorithm (shortest CPU time first).
        Start two consumer threads to execute the jobs by sleeping for the required CPU time.
        Print the job executed by each consumer and their total CPU time.

How the Cluster Works

    The head node thread listens for incoming jobs from the embedded device. It extracts the process name and CPU time from each message and adds the job to a shared queue.
    The jobs in the queue are sorted by CPU time to implement the Shortest Job First scheduling algorithm.
    The consumer threads pick jobs from the queue (using a semaphore to block until jobs are available) and simulate job execution by sleeping for the duration of the CPU time.
    Each consumer keeps track of the jobs they execute and the total CPU time consumed.

Example Output from the Cluster:

less

Accepted connection from ('127.0.0.1', 54872)
Job added and sorted: [('top', 3), ('ls', 1)]
Job added and sorted: [('ls', 1), ('top', 3), ('cut', 5)]
Consumer 1 executing ls for 1 seconds
Consumer 2 executing top for 3 seconds
Consumer 1 executing cut for 5 seconds
Consumer 1 total time: 6
Consumer 2 total time: 3

References

    Python Threading: Official documentation on Python's threading module: https://docs.python.org/3/library/threading.html
    Python Sockets: Official documentation on Python's socket module for TCP communication: https://docs.python.org/3/library/socket.html
    psutil Library (if used): Documentation for psutil, which provides information about system and process utilities: https://psutil.readthedocs.io/en/latest/

Contributors

This project was developed as part of the Operating Systems course at the University of Puerto Rico, Río Piedras campus.

    Student Name: [Your Name Here]
    Verbal Collaborators: [List any classmates or students you consulted with during the project, if applicable.]
