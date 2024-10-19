# MIT License
#
# Copyright (c) 2021 God Empress Verin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from pwpy import errors

import typing
import aiohttp
import asyncio
import time
import logging
import contextlib
import json


_LOGGER = logging.getLogger("pwpy.events")


__all__: typing.List[str] = [
    "get_query",
    "BulkQuery",
    "SocketWrapper",
    "QueryWrapper",
]


def _ratelimit(func):
    remaining: int = 0
    reset: int = 0

    async def wrapper(*args, **kwargs):
        nonlocal remaining
        nonlocal reset

        if remaining == 0:
            await asyncio.sleep(reset - time.time())

        try:
            result: dict = await func(*args, **kwargs)

        except errors.RateLimitHit as exc:
            remaining = int(exc.headers["X-RateLimit-Remaining"])
            reset = int(exc.headers["X-RateLimit-Reset"])
            result: dict = await wrapper(*args, **kwargs)

        return result

    return wrapper


def _convert_args_to_string(args: dict) -> typing.Generator:
    """Converts dict of args to string."""
    for key, value in args.items():
        if isinstance(value, str):
            yield f'{key}:"{value}"'

        else:
            yield f'{key}:{value}'


def _convert_sequence_to_string(field_data: typing.Sequence) -> typing.Generator:
    """Converts tuples/lists into strings."""
    for field in field_data:
        if isinstance(field, dict):
            yield ' '.join(_convert_fields_to_string(field))

        elif isinstance(field, str):
            yield field


def _convert_fields_to_string(data: typing.Union[str, dict, typing.Sequence]) -> typing.Generator:
    """Converts the data fields into a string."""
    if isinstance(data, dict):
        for field_name, field_value in data.items():
            if isinstance(field_value, str):
                yield f"{field_name} {{{field_value}}}"

            elif isinstance(field_value, typing.Sequence):
                converted_fields: str = ' '.join(_convert_sequence_to_string(field_value))
                yield f"{field_name} {{{converted_fields}}}"

    elif isinstance(data, str):
        yield f"data{{{data}}}"

    elif isinstance(data, typing.Sequence):
        yield ' '.join(_convert_sequence_to_string(data))

    else:
        raise TypeError("fields must be of type str, dict, or typing.Sequence!")


def _convert_dict_to_query(query_data: typing.Union[str, dict]) -> str:
    """
    Convert a properly formatted dict into a graphql string.

    :param query_data: A properly formatted GQL string or a dict that can be converted into a GQL string.
    :return: A converted GQL string or the provided query string.
    """
    if isinstance(query_data, str):
        return query_data

    converted_query: str = f"{query_data['model']}"

    if query_args := query_data.get("args"):
        converted_args: str = ' '.join(_convert_args_to_string(query_args))
        converted_query += f"({converted_args}) "

    if query_fields := query_data.get("fields"):
        converted_fields: str = ' '.join(_convert_fields_to_string(query_fields))
        converted_query += f"{{{converted_fields}}}"

    return converted_query


def _raise_message_exception(_errors: list) -> None:
    message: str = _errors[0]["message"]

    if "cannot query field" in message:
        raise errors.QueryFieldError(message)

    elif "must have a sub selection" in message:
        raise errors.QueryMissingSubSelection(message)

    elif "syntax error" in message:
        raise errors.QuerySyntaxError(message)

    elif "unknown argument" in message:
        raise errors.QueryArgumentInvalid(message)

    else:
        raise errors.UnexpectedResponse(message)


def _raise_status_exception(status, headers) -> None:
    if status in (520, 521, 522):
        raise errors.CloudflareError(status)

    elif status == 401:
        raise errors.QueryKeyError("you specified an invalid api_key.")

    elif status == 503:
        raise errors.ServiceUnavailable()

    elif status == 429:
        raise errors.RateLimitHit(headers)


@_ratelimit
async def get_query(query: typing.Union[str, dict], api_key: str) -> dict:
    """
    Post a GQL query, parsing for errors and returning the data.

    :param query: A properly formatted GQL string or a dict that can be converted into a GQL string.
    :param api_key: A valid Politics And War API key.
    :return: API response data.
    """
    payload: dict = {"api_key": api_key, "query": f"{{{_convert_dict_to_query(query)}}}"}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.politicsandwar.com/graphql", json=payload) as response:
            _raise_status_exception(response.status, response.headers)
            response_data: dict = await response.json()

    if _errors := response_data.get("errors"):
        _raise_message_exception(_errors)

    elif data := response_data.get("data"):
        return data

    else:
        raise errors.ResponseFormatError(str(response_data))


class BulkQuery:
    """
    Build, chunk, and post mass queries.
    """
    def __init__(self, api_key: str, *, chunk_size: int = 10):
        """
        :param api_key: A valid Politics And War API key.
        :param chunk_size: The number of queries to send in each payload.
        """
        self._api_key: str = api_key
        self._queries: set = set()

        if chunk_size < 1:
            raise ValueError("chunk size must be one or higher!")

        self._chunk_size: int = chunk_size

    @property
    def _chunk_requests(self) -> typing.Generator:
        """
        Splits the queries into chunks.

        :return: Groups of joined GQL query strings.
        """
        payloads: list = list(self._queries)
        chunk_size: int = self._chunk_size

        for count in range(0, len(payloads), chunk_size):
            chunk: set[str] = set()

            for payload in payloads[count:count + chunk_size]:
                chunk.add(payload)

            yield "\n".join(chunk)

    def insert(self, query: typing.Union[dict, str]) -> None:
        """
        Attach a query or list of queries to the bulk query request.

        :param query: A properly formatted GQL string or a dict that can be converted into a GQL string.
        """
        self._queries.add(_convert_dict_to_query(query))

    async def get(self) -> dict:
        """
        Post the bulk GQL query, parsing for errors and returning the data.

        :return: A dict containing all returned API response data.
        """
        results: dict = dict()
        tasks: list = list()

        async with asyncio.TaskGroup() as tg:
            for chunk in self._chunk_requests:
                tasks.append(tg.create_task(get_query(chunk, self._api_key)))

        for task in tasks:
            results.update(task.result())

        return results


class Listener:

    def __init__(self, coro: typing.Coroutine, model: str, event: str) -> None:
        self.coro: typing.Coroutine = coro
        self.model: str = model
        self.event: str = event
        self.channel: typing.Optional[str] = None
        self.active: asyncio.Event = asyncio.Event()


class SocketWrapper:
    def __init__(self, api_key: str, *, loop: typing.Optional[asyncio.BaseEventLoop] = None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self._api_key: str = api_key
        self._tasks: typing.Set[asyncio.Task] = set()
        self._loop = loop
        self._running: bool = False
        self._closing: asyncio.Event = asyncio.Event()
        self._session: typing.Optional[aiohttp.ClientSession] = None
        self._socket: typing.Optional[aiohttp.ClientWebSocketResponse] = None
        self._socket_id: typing.Optional[str] = None
        self._connected: asyncio.Event = asyncio.Event()
        self._listening: asyncio.Event = asyncio.Event()
        self._reconnecting: bool = False
        self._timeout: int = 120
        self._last_msg: float = 0
        self._last_ping: float = 0
        self._last_pong: float = 0
        self._listeners: typing.Dict[Listener] = dict()
        self._listener: typing.Optional[asyncio.Task] = None
        self._heartbeat: typing.Optional[asyncio.Task] = None

    def _create_task(self, coro: typing.Coroutine):
        def done_callback(_):
            self._tasks.remove(task)

        task = self._loop.create_task(coro, name=coro.__name__)
        task.add_done_callback(done_callback)
        self._tasks.add(task)

    async def run(self):
        if self._running:
            raise errors.WatcherStateError("watcher is already running!")

        elif self._closing.is_set():
            await self._closing.wait()

        await self._connect()

        self._listener = self._loop.create_task(self._listen_for_messages())
        self._heartbeat = self._loop.create_task(self._ensure_heartbeat())

        self._running = True

    async def stop(self):
        if not self._running:
            raise errors.WatcherStateError("watcher is not currently running!")

        elif self._closing.is_set():
            raise errors.WatcherStateError("watcher is already closing!")

        self._running = False
        self._closing.set()

        self._listener.cancel()
        self._heartbeat.cancel()

        await self._maybe_close_socket()

        if self._tasks:
            done, pending = await asyncio.wait(self._tasks, timeout=120)

            for task in pending:
                task.cancel()

        if self._session and not self._session.closed:
            await self._session.close()

        self._closing.clear()

    async def _connect(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

            if self._socket:
                await self._maybe_close_socket()

        self._socket = await self._session.ws_connect(
            "wss://socket.politicsandwar.com/app/a22734a47847a64386c8?protocol=7",
            timeout=30,
            autoclose=False,
            max_msg_size=0
        )
        self._connected.set()

    async def _reconnect(self, message: bytes = b""):
        if self._reconnecting:
            return

        self._reconnecting = True

        await self._maybe_close_socket(1002, message)

        self._last_msg = time.perf_counter()
        self._last_ping = time.perf_counter()
        self._last_pong = time.perf_counter() + 1

        await self._connect()

        for channel, listener in self._listeners.items():
            self._create_task(self._subscribe(listener))

        self._reconnecting = False

    async def _maybe_close_socket(self, code: int = 1000, message: bytes = b""):
        self._connected.clear()
        self._listening.clear()

        if self._socket.closed:
            return

        with contextlib.suppress(ConnectionResetError):
            await self._socket.close(code=code, message=message)

    async def _handle_closed_socket(self):
        self._connected.clear()
        self._listening.clear()

        close_code = self._socket.close_code

        if close_code in range(4000, 4100):
            await asyncio.sleep(600)

        elif close_code in range(4100, 4200):
            await asyncio.sleep(1)

        await self._reconnect()

    async def _handle_message(self, message):
        if message.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING):
            await self._handle_closed_socket()

        elif message.type != aiohttp.WSMsgType.TEXT:
            _LOGGER.warning("message of unknown type was received! (%s)", message.type)

            return

        data = json.loads(message.data)
        event = data["event"]

        self._last_msg = time.perf_counter()

        if event == "pusher:connection_established":
            event_data = json.loads(data["data"])
            self._socket_id = event_data["socket_id"]
            self._timeout = min(self._timeout, event_data["activity_timeout"])
            self._listening.set()

        elif event == "pusher_internal:subscription_succeeded":
            if listener := self._listeners.get(data["channel"]):
                listener.active.set()

            else:
                await self._unsubscribe(data["channel"])

        elif event == "pusher:pong":
            self._last_pong = time.perf_counter()

        elif event == "pusher:ping":
            await self._send_message("pusher:pong")

        else:
            if listener := self._listeners.get(data["channel"]):
                event_data = json.loads(data["data"])
                await listener.coro(listener, event_data)

            else:
                await self._unsubscribe(data["channel"])

    async def _send_message(self, event: str, data: dict = None):
        payload = {"event": event, "data": data or {}}
        await self._socket.send_json(payload)

    async def _listen_for_messages(self):
        while True:
            await self._connected.wait()

            async for message in self._socket:
                self._create_task(self._handle_message(message))

            if self._socket.closed:
                await self._handle_closed_socket()

    async def _ensure_heartbeat(self):
        while True:
            try:
                sleep_time = self._last_msg + self._timeout - time.perf_counter()

                if sleep_time < 0:
                    await asyncio.sleep(1)

                    continue

                await asyncio.sleep(sleep_time)

                if self._last_msg + self._timeout > time.perf_counter():
                    continue

                if self._last_ping > self._last_pong:
                    if self._last_ping + self._timeout < time.perf_counter():
                        await self._reconnect()

                        await asyncio.sleep(self._timeout)

                    continue

                if self._last_ping + self._timeout > time.perf_counter():
                    continue

                await self._send_message("pusher:ping")

                self._last_ping = time.perf_counter()

            except ConnectionResetError:
                await self._reconnect(b"Connection reset")

                await asyncio.sleep(self._timeout)

    async def _request_channel(self, listener: Listener):
        url = "https://api.politicsandwar.com/subscriptions/v1/subscribe/{model}/{event}"
        url = url.format(model=listener.model, event=listener.event)

        async with self._session.get(
            url,
            params={"api_key": self._api_key}
        ) as response:
            try:
                data = await response.json()

                if error_msg := data.get("error"):
                    raise errors.SubscribeFailed(error_msg)

                listener.channel = data["channel"]

            except aiohttp.ContentTypeError as exc:
                raise errors.SubscribeFailed(exc.message) from exc

    async def _authorize_subscribe(self, listener: Listener):
        payload = {"socket_id": self._socket_id, "channel_name": listener.channel}

        async with self._session.post(
            "https://api.politicsandwar.com/subscriptions/v1/auth",
            data=payload
        ) as response:
            if response.status != 200:
                raise errors.AuthorizeFailed()

            data = await response.json()

            return data["auth"]

    async def _subscribe(self, listener: Listener):
        if not listener.channel:
            await self._request_channel(listener)

        try:
            auth = await self._authorize_subscribe(listener)

        except errors.AuthorizeFailed:
            await self._request_channel(listener)
            auth = await self._authorize_subscribe(listener)

        data = {"auth": auth, "channel": listener.channel}
        await self._send_message("pusher:subscribe", data)

        try:
            self._listeners[listener.channel] = listener
            await asyncio.wait_for(listener.active.wait(), timeout=60)

        except asyncio.TimeoutError:
            self._listeners.pop(listener.channel, None)

            raise errors.SubscribeFailed()

    async def subscribe(self, listener: Listener):
        if self._closing.is_set():
            raise errors.WatcherStateError()

        elif self._running and self._socket.closed:
            await self._reconnect()

        if not self._listening.is_set():
            await self._listening.wait()

        await self._subscribe(listener)

    async def _unsubscribe(self, channel: str):
        self._listeners.pop(channel, None)
        await self._send_message("pusher:unsubscribe", {"channel": channel})

    async def unsubscribe(self, listener: Listener):
        await self._unsubscribe(listener.channel)

    def listen(self, model: str, event: str):
        def decorator(coro: typing.Coroutine):
            listener = Listener(coro, model, event)
            self._create_task(self.subscribe(listener))

            return coro

        return decorator


class QueryWrapper:

    def __init__(self, api_key: str) -> None:
        self._api_key: str = api_key
        self._watcher: typing.Optional[SocketWrapper] = None

    async def get_query(self, query: typing.Union[str, dict]) -> dict:
        return await get_query(query, self._api_key)

    def bulk_query(self, *, chunk_size: int = 10) -> BulkQuery:
        return BulkQuery(self._api_key, chunk_size=chunk_size)
