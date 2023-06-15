from channels.middleware import BaseMiddleware


class HeaderMiddleware(BaseMiddleware):
    """
    Forms headers to a dict.
    """

    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        scope["headers_dict"] = {
            key.decode("utf-8"): value.decode("utf-8")
            for key, value in scope["headers"]
        }
        return await super().__call__(scope, receive, send)
