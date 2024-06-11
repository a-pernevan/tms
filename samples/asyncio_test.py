import asyncio

async def web_server():
    # Your web server logic here
    for i in range(5):
        print("Hello")
        await asyncio.sleep(1)  # Yield control to other tasks

async def relay_event_loop():
    # Your relay control logic here
    for i in range(5):
        print("Relay")
        await asyncio.sleep(0.5)  # Yield control to other tasks

# Start the event loop
loop = asyncio.get_event_loop()
# loop.create_task(web_server())
# loop.create_task(relay_event_loop())
# loop.run_forever()
loop.run_until_complete(web_server())  
loop.run_until_complete(relay_event_loop())