from aiohttp import web
import socketio
import requests
from database import Database
import os
from dotenv import load_dotenv

load_dotenv()

RASA_SERVER = os.getenv('RASA_SERVER')

print(RASA_SERVER)

messages = [
    "action_cung_cap_ten_san_pham",
    "action_provide_product_name",
    "action_cung_cap_sdt_tra_cuu_don_hang",
    "action_provide_phone_number_to_check_order",
]

sio = socketio.AsyncServer(cors_allowed_origins="*")
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
    actions = text.split("|")
    action = actions[0]
    keyword = actions[1]
    if action == "action_cung_cap_ten_san_pham":
        # get product name with `text`
        query = f"select name,price,slug from products where lower(name) like lower('%{keyword}%') limit 5;".format(
            keyword=keyword
        )

        print(query)

        result = executeQuery(query)

        if result is None:
            return ["Xin lỗi, chúng tôi không tìm thấy sản phẩm này."]

        result_nraw = []
        for r in result:
            result_nraw.append(
                "Sản phẩm {name} có giá là {price}.".format(name=r[0], price=r[1])
            )

        return result_nraw

    if action == "action_cung_cap_sdt_tra_cuu_don_hang":
        # get order with `text`
        query = f"select id,user_id,status from orders limit 5;".format(keyword=keyword)

        result = executeQuery(query)

        if result is None:
            return ["Xin lỗi, chúng tôi không tìm thấy đơn hàng này."]

        result_nraw = []
        for r in result:
            result_nraw.append(
                "Đơn hàng {id} được đặt bởi {phone} có trạng thái là {status}.".format(
                    id=r[0], phone=r[1], status=r[2]
                )
            )

        return result_nraw

    if action == "action_provide_product_name":
        # get product name with `text`
        query = f"select name,price,slug from products where lower(name) like lower('%{keyword}%') limit 5;".format(
            keyword=keyword
        )

        result = executeQuery(query)

        if result is None:
            return ["Xin lỗi, chúng tôi không tìm thấy sản phẩm này."]

        result_nraw = []
        for r in result:
            result_nraw.append(
                "Sản phẩm {name} có giá là {price}.".format(name=r[0], price=r[1])
            )

        return result

    if action == "action_provide_phone_number_to_check_order":
        # get order with `text`
        query = f"select id,user_id,status from orders limit 5;".format(keyword=keyword)

        result = executeQuery(query)

        if result is None:
            return ["Xin lỗi, chúng tôi không tìm thấy đơn hàng này."]

        result_nraw = []
        for r in result:
            result_nraw.append(
                "Đơn hàng {id} được đặt bởi {phone} có trạng thái là {status}.".format(
                    id=r[0], phone=r[1], status=r[2]
                )
            )

        return result_nraw


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def send(sid, data):
    response = requests.post(
        RASA_SERVER + "/webhooks/rest/webhook",
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
