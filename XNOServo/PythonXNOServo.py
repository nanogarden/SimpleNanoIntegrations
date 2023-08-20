import asyncio
import websockets
import json
import serial


host = '0.0.0.0' # The host. If running a local node in the same computer, then 0.0.0.0 is appropriate 
port = '7078' # The default websocket port

arduino = serial.Serial('/dev/ttyUSB0', 115200) # Change 'dev/ttyUSB0' to your arduino port

receiver = "nano_165ncyhzggm6d9isrhfu956s6dnrt3tca8dge86b4uw97zddmt9cfwzyo63i" # The address that must receive the amount to trigger the action

required_amount = "1" + "0"*30 # String holding the amount of RAW that the transaction must contain, in this case 1 nano (1E30 RAW)


def subscription(topic: str, ack: bool=False, options: dict=None):
    d = {"action": "subscribe", "topic": topic, "ack": ack}
    if options is not None:
        d["options"] = options
    return d

async def main():
    async with websockets.connect(f"ws://{host}:{port}") as websocket:

        await websocket.send(json.dumps(subscription("confirmation", options={"include_election_info": "false", "include_block":"true","accounts": [receiver]}, ack=True)))
        print(await websocket.recv()) # ack


        while 1:
            rec = json.loads(await websocket.recv())
            topic = rec.get("topic", None)
            if topic:
                message = rec["message"]
                amount = message["amount"]
                subtype = message["block"]["subtype"]
                link = message["block"]["link_as_account"]
                print(amount)
                if (subtype == "send") & (link == receiver) & (message["amount"] == required_amount):
                 arduino.write(b'trigger')
                 print('Success!')

try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    pass
except ConnectionRefusedError:
    print("Error connecting to websocket server. [node.websocket] enable=true must be set in ~/Nano/config-node.toml ; see host/port options with ./client.py --help")

