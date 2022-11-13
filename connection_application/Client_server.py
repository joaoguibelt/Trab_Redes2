import socket


def cli_ser():
    # Get the IP address of the register server
    register_server = input("Enter the IP address of the register server: ")

    # Connect to the register server
    register_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if register_socket.connect((register_server, 5000)) == 1:
        print("Server not found")

    # Get the IP address of the user to connect to
    user = input("Enter the IP address of the user to connect to: ")

    # Send the IP address of the user to connect to the register server
    register_socket.send(user.encode())

    # Get the IP address of the user to connect to from the register server
    user = register_socket.recv(1024).decode()

    # Close the connection with the register server
    register_socket.close()

    # Connect to the user to connect to
    user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if user_socket.connect((user, 5000)) == 1:
        print("Server not found")

    # Close the connection with the user to connect to
    user_socket.close()

    # End of the function
