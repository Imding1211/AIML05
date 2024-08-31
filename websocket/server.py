import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    # 添加新客戶端到連接的客戶端列表中
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from mange.py: {message}")
            # 將收到的消息發送給所有已連接的客戶端
            await asyncio.gather(*[client.send(message) for client in connected_clients])
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        # 客戶端斷開連接後，從連接的客戶端列表中移除
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # 保持服務器運行

if __name__ == "__main__":
    asyncio.run(main())
