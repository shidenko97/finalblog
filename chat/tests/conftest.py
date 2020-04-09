import pytest

from chat.main import init_app, ANONYMOUS_AVATAR, ANONYMOUS_NAME


# Sets of user for testing
CHAT_USER_SET = [
    (
        {"username": "Odin", "avatar": "Cool image here"},
        None,
    ),
    (
        None,
        {"username": "Thor", "avatar": "Mjölnir"},
    ),
]


@pytest.fixture(params=CHAT_USER_SET)
async def get_clients(request, test_client) -> tuple:
    """
    Get web sockets and their names and avatars (one named and one anonymous)
    :param request: Request of fixture
    :type request: __pytest.fixtures.SubRequest
    :param test_client: Client factory function
    :type test_client: func
    :return:
    """

    users = request.param

    app = await init_app()
    client = await test_client(app)

    if users[0] is None:
        ws1 = await client.ws_connect("/")
        ws2 = await client.ws_connect(f"?username={users[1]['username']}&"
                                      f"avatar={users[1]['avatar']}")

        return (ws1, ws2, ANONYMOUS_NAME, ANONYMOUS_AVATAR,
                users[1]['username'], users[1]['avatar'])

    ws1 = await client.ws_connect(f"?username={users[0]['username']}&"
                                  f"avatar={users[0]['avatar']}")
    ws2 = await client.ws_connect("/")

    return (ws1, ws2, users[0]['username'], users[0]['avatar'],
            ANONYMOUS_NAME, ANONYMOUS_AVATAR)
