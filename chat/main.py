from aiohttp import web, WSMsgType


# Data for anonymous user
ANONYMOUS_AVATAR = ("https://cdn2.iconfinder.com/data/icons/social-messaging-"
                    "productivity-black-2/21/07-512.png")
ANONYMOUS_NAME = "Anonymous"


async def init_app() -> web.Application:
    """
    Function that initiate a chat application
    :return: Application instance
    :rtype: web.Application
    """

    # Initiate chat application
    app = web.Application()

    # Initiate websockets' storage
    app["websockets"] = {}

    # Add `on shutdown` event handler
    app.on_shutdown.append(shutdown)

    # Add main route of application
    app.router.add_get("/", index)

    return app


async def shutdown(app: web.Application):
    """
    Close all websockets on shutdown and flush the dict of websockets
    :param app: Application instance
    :type app: web.Application
    """

    for ws in app["websockets"].values():
        await ws.close()

    app["websockets"].clear()


async def index(request: web.Request) -> web.WebSocketResponse:
    """
    Main view for the chat
    :param request: Dict-like object that contains all the information about
    incoming request
    :type request: web.Request
    :return: Return of websocket
    :rtype: web.WebSocketResponse
    """

    ws_current = web.WebSocketResponse()

    await ws_current.prepare(request)

    # Define name and avatar for each user
    name = request.rel_url.query.get("username", ANONYMOUS_NAME)
    avatar = request.rel_url.query.get("avatar", ANONYMOUS_AVATAR)

    # Send a `connected` signal connected user
    await ws_current.send_json({'action': 'connect', 'avatar': avatar,
                                'name': name})

    # Send a `connected` signal to all chat users
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'join', 'avatar': avatar, 'name': name})
    request.app['websockets'][name] = ws_current

    # Main chat loop
    while True:
        msg = await ws_current.receive()

        # If handled a text message - send it to all users except current
        # but if handled another type of message - break a loop and close
        # current connection
        if msg.type == WSMsgType.text:
            for ws in request.app['websockets'].values():
                if ws is not ws_current:
                    await ws.send_json(
                        {'action': 'sent', 'avatar': avatar, 'name': name,
                         'text': msg.data})
        else:
            break

    # Delete connection from storage and send `disconnected` message to other
    # users of chat
    del request.app['websockets'][name]
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'disconnect', 'avatar': avatar,
                            'name': name})

    return ws_current


def main():
    """
    Run application function
    """
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
