import asyncio


class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)


async def main():
    server1 = await asyncio.start_server(
        EchoProtocol, '127.0.0.1', 8888)

    addr1 = server1.sockets[0].getsockname()
    print(f'Serving 1 on {addr1}')

    server2 = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8889)

    addr2 = server2.sockets[0].getsockname()
    print(f'Serving 2 on {addr2}')

    async with server1, server2:
        await asyncio.gather(
            server1.serve_forever(), server2.serve_forever())

asyncio.run(main())
