from chat.tests.conftest import get_clients  # noqa: F401


async def test_connection(get_clients: tuple):  # noqa: F811
    """
    Test connection to chat
    :param get_clients: Sockets of two users and their usernames and avatars
    :param get_clients: tuple
    """

    ws1, ws2, username1, avatar1, username2, avatar2 = get_clients

    # Check first socket connection message to oneself
    ack_msg1 = await ws1.receive()
    assert ack_msg1.json()["action"] == "connect"
    assert ack_msg1.json()["name"] == username1
    assert ack_msg1.json()["avatar"] == avatar1

    # Check second socket connection message to oneself
    ack_msg2 = await ws2.receive()
    assert ack_msg2.json()["action"] == "connect"
    assert ack_msg2.json()["name"] == username2
    assert ack_msg2.json()["avatar"] == avatar2

    # Check first socket connection message to second socket
    ack_msg3 = await ws1.receive()
    assert ack_msg3.json()["action"] == "join"
    assert ack_msg3.json()["name"] == username2
    assert ack_msg3.json()["avatar"] == avatar2


async def test_message(get_clients: tuple):  # noqa: F811
    """
    Test sending message to chat
    :param get_clients: Sockets of two users and their usernames and avatars
    :param get_clients: tuple
    """

    ws1, ws2, username1, avatar1, username2, avatar2 = get_clients

    # Skip connection messages
    await ws1.receive()
    await ws2.receive()
    await ws1.receive()

    # First socket send message
    text_to_send = "Hi all"
    await ws1.send_str(text_to_send)
    received_msg = await ws2.receive()
    received_dict = received_msg.json()

    # Check received message from first socket
    assert received_dict["text"] == text_to_send
    assert received_dict["name"] == username1
    assert received_dict["avatar"] == avatar1

    # Second socket send message
    text_to_send1 = "Hi, friend"
    await ws2.send_str(text_to_send1)
    received_msg1 = await ws1.receive()
    received_dict1 = received_msg1.json()

    # Check received message from second socket
    assert received_dict1["text"] == text_to_send1
    assert received_dict1["name"] == username2
    assert received_dict1["avatar"] == avatar2


async def test_disconnection(get_clients: tuple):  # noqa: F811
    """
    Test disconnection from chat
    :param get_clients: Sockets of two users and their usernames and avatars
    :param get_clients: tuple
    """

    ws1, ws2, username1, avatar1, username2, avatar2 = get_clients

    # Skip connection messages
    await ws1.receive()
    await ws2.receive()
    await ws1.receive()

    # Close connection of first socket
    await ws1.close()

    # Check disconnect message from first socket
    ack_msg2 = await ws2.receive()
    assert ack_msg2.json()["action"] == "disconnect"
    assert ack_msg2.json()["name"] == username1
    assert ack_msg2.json()["avatar"] == avatar1
