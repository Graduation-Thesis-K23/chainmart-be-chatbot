from aiohttp import web
import socketio
import requests

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def send(sid, data):
    response = requests.post(
        "http://rasa:5005/webhooks/rest/webhook",
        json={"sender": sid, "message": data},
    ).json()

    print("response ", response)
    await sio.emit("receive", response[0]["text"], room=response[0]["recipient_id"])


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    web.run_app(app, port=5000)
