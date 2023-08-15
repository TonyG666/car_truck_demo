import asyncio
import websockets
import json
from pymongo import MongoClient

print('start')

client = MongoClient("localhost", 27017)

async def handle_request(websocket, path):
    async for message in websocket:
        try:
            request = json.loads(message)
            if "method" in request and request["method"] == "GET":
                key = request["params"]["key"]
                value = request["params"]["value"] #a dictionary
                db = client["demo"]
                collection = db[key]
                cols = [val for val in value.values()]
                result = {col: collection[col] for col in cols}
                if result:
                    response = {"data": result}
                else:
                    response = {"error": "Data not found"}
            else:
                response = {"error": "Invalid request"}
            await websocket.send(json.dumps(response))
        except Exception as e:
            response = {"error": str(e)}
            await websocket.send(json.dumps(response))

start_server = websockets.serve(handle_request, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

print('end')


# import asyncio
 
# import websockets
 
# # create handler for each connection
 
# async def handler(websocket, path):
 
#     data = await websocket.recv()
 
#     reply = f"Data recieved as:  {data}!"
 
#     await websocket.send(reply)
 
 
 
# start_server = websockets.serve(handler, "localhost", 8000)
 
 
 
# asyncio.get_event_loop().run_until_complete(start_server)
 
# asyncio.get_event_loop().run_forever()

