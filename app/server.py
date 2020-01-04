import traceback

from app import client_handler
from app.cli import CommandLineInterface
from app.utils.listener import Listener

cli = CommandLineInterface()


def run_server(address, data_dir):
    listener = Listener(address[1], address[0])
    listener.start()
    # server = socket.socket()
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server.bind(address)
    # server.listen()

    while True:
        connection = listener.accept()
        handler = client_handler.Handler(connection, data_dir)
        # conn, addr = server.accept()
        # handler = client_handler.Handler(conn, data_dir)
        handler.start()


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        address = argv[1].split(":")
        address_as_tuple = (address[0], int(address[1]))
        run_server(address_as_tuple, argv[2])
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        print(traceback.format_exc())
        return 1


@cli.command
def run(address, data):
    address_lst = address.split(":")
    address_as_tuple = (address_lst[0], int(address_lst[1]))
    run_server(address_as_tuple, data)
    print('done')


if __name__ == '__main__':
    cli.main()
