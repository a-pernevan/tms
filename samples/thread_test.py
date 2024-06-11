import threading
import time

def my_task():
    for i in range(5):
        print(f"Thread {threading.current_thread().name}: {i}")
        time.sleep(0.1)

# Create two threads
thread1 = threading.Thread(target=my_task, name="Thread 1")
thread2 = threading.Thread(target=my_task, name="Thread 2")

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Main thread exiting")
