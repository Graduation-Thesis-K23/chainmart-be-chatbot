from aiohttp import web
import socketio
import requests
from database import Database

messages = [
    "action_cung_cap_ten_san_pham",
    "action_provide_product_name",
    "action_cung_cap_sdt_tra_cuu_don_hang",
    "action_provide_phone_number_to_check_order",
]

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


def executeQuery(query):
    db = Database()
    db.connect()
    cur = db.conn.cursor()
    cur.execute(query)

    rows = cur.fetchall()

    cur.close()
    db.disconnect()

    # check if rows is empty
    if len(rows) == 0:
        return None

    return rows


def processMessage(text):
    action, text = text.split("|")
    if action == "action_cung_cap_ten_san_pham":
        # get product name with `text`
        query = (
            "select * from products where lower(name) like lower('%{text}%') limit 5".format(
                text=text
            )
        )

        return executeQuery(query)
    if action == "action_cung_cap_sdt_tra_cuu_don_hang":
        # get order with `text`
        query = "select * from orders where phone_number = '{text}' limit 5".format(text=text)

        return executeQuery(query)

    if action == "action_provide_product_name":
        # get product name with `text`
        query = (
            "select * from products where lower(name) like lower('%{text}%' limit 5)".format(
                text=text
            )
        )

        return executeQuery(query)

    if action == "action_provide_phone_number_to_check_order":
        # get order with `text`
        query = "select * from orders where phone_number = '{text}' limit 5".format(text=text)

        return executeQuery(query)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def send(sid, data):
    response = requests.post(
        "http://rasa:5005/webhooks/rest/webhook",
        json={"sender": sid, "message": data},
    ).json()

    if len(response) == 0:
        sio.emit(
            "receive",
            "Xin lỗi, chúng tôi không hiểu yêu cầu của bạn. Vui lòng liên hệ 0984526014 để gặp tư vấn viên.",
            room=sid,
        )
        return

    text = response[0]["text"]

    if "|" in text:
        res = processMessage(text)

        for e in res:
            await sio.emit("receive", e, room=sid)

    else:
        await sio.emit("receive", response[0]["text"], room=response[0]["recipient_id"])


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    web.run_app(app, port=5000)
