from miniboa import TelnetServer
from go import Go

server = TelnetServer()

IDLE_TIMEOUT = 300
CLIENT_LIST = []
CLIENT_GO = dict()
SERVER_RUN = True


# Chat demo: https://github.com/jimstorch/miniboa/blob/master/chat_demo.py

def on_connect(client):
    client.send("HELLO! Welcome to this silly GNUGO middleware :)\n")
    print("Connected: ", client.addrport())
    client.send("Size of the board?\n")
    CLIENT_LIST.append(client)
    CLIENT_GO[client.addrport()] = None


def on_disconnect(client):
    print("Disconnected: ", client.addrport())
    del CLIENT_GO[client.addrport()]
    CLIENT_LIST.remove(client)


def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in CLIENT_LIST:
        client.send(msg)


def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            cl_name = client.addrport()
            print("[{}] Sent a message\n".format(cl_name))
            # If the client sends input echo it to the chat room
            go = CLIENT_GO[cl_name]
            move = client.get_command()
            if move != "q":
                if go is not None:
                    if go.status == 0:
                        print("[{}] in status 0. Move: {}".format(
                            cl_name, move))
                        msg = go.go_black_round(move)
                        client.send(msg)
                        if go.status == 1:  # If the move was legal
                            client.send("Press enter to continue\n")
                        else:
                            client.send(go.go_black_round_init())
                    elif go.status == 1:
                        print("[{}] in status 1".format(cl_name))
                        client.send("Thinking...\n")
                        client.send(go.go_white_round())
                        client.send(go.go_black_round_init())
                    elif go.status == 2:
                        client.send("Game finished!")
                        # TODO: restart
                        client.active = False

                else:
                    # Init Go
                    try:
                        size = int(move)
                        if size > 3 and size < 21:
                            CLIENT_GO[client.addrport()] = Go(size=size)
                            go = CLIENT_GO[client.addrport()]
                            client.send(go.print_board())
                            client.send(go.go_black_round_init())
                        else:
                            client.send("Wrong size. 3 < size < 21\n")
                    except ValueError:
                        client.send("Wrong size. 3 < size < 21\n")
            else:
                client.send("BYE!")
                client.active = False


server = TelnetServer(
    port=5000,
    address='',
    on_connect=on_connect,
    on_disconnect=on_disconnect)


# Server Loop
while SERVER_RUN:
    server.poll()        # Send, Recv, and look for new connections
    process_clients()    # Check for client input

print(">> Server shutdown.")
