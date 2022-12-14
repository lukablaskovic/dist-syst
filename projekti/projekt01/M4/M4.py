import aiofiles
import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

received_code = []

print("M4 running...")


@ routes.post("/gatherData")
async def gatherData(req):
    try:
        record = await req.json()
        print("Code received and stored! ✅")
        code = record["content"]
        username = record["username"]
        received_code.append({"username": username, "code": code})

        if len(received_code) > 10:
            await saveToFiles()

        return web.json_response({"M4": "OK"}, status=200)
    except Exception as e:
        return web.json_response({"M4": str(e)}, status=500)


async def saveToFiles():
    print("Started saving files... 📂")
    try:
        for item in received_code:
            async with aiofiles.open('app/files/{username}.txt'.format(username=item["username"]), 'w') as f:
                await f.write(item["code"])
        received_code.clear()
        print("Files successfuly saved and list cleaned! 📁")
    except Exception as e:
        print(e)
    pass

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=1200)
