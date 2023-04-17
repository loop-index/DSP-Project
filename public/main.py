import api_main, db_main
import signal

# Handler function for when the program is terminated
def terminate_handler(signal, frame):
    print('Terminating server...')
    api_main.stop_server()
    db_main.shutdown()
    exit(0)

if __name__ == '__main__':
    # Run Flask server
    api_main.run_server()

    # Register handler for termination
    signal.signal(signal.SIGINT, terminate_handler)