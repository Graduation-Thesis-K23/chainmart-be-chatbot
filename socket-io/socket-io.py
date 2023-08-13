from aiohttp import web
import socketio
import requests

# from database import Mongo
# from database import Postgres
import os
from dotenv import load_dotenv
from unidecode import unidecode

load_dotenv()

# RASA_SERVER = str(os.getenv("RASA_URL"))

# print('RASA SERVER: ', RASA_SERVER)
RASA_SERVER = str(os.getenv("rasa_uri"))
CHAINMART_BE = str(os.getenv("chainmart_be"))

print(RASA_SERVER)
print(CHAINMART_BE)

messages = [
    "action_cung_cap_ten_san_pham",
    "action_provide_product_name",
    "action_cung_cap_sdt_tra_cuu_don_hang",
    "action_provide_phone_number_to_check_order",
]

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)


# def executeQueryPostgres(query):
#     db = Postgres()
#     db.connect()
#     cur = db.conn.cursor()
#     cur.execute(query)

#     rows = cur.fetchall()

#     cur.close()
#     db.disconnect()

#     # check if rows is empty
#     if len(rows) == 0:
#         return None

#     return rows


def executeQueryMongo(query, collection_name):
    db = Mongo()
    collection = db.database[collection_name]

    result = collection.find(query)

    rows = []

    for r in result:
        rows.append(r)

    # check if rows is empty
    if len(rows) == 0:
        return None

    return rows


def processMessage(text):
    actions = text.split("|")
    action = actions[0]
    keyword = actions[1]

    print(text)

    if action == "action_cung_cap_ten_san_pham":
        # item = keyword.strip().lower()
        # query = { "name" : f"/.*{item}*./"}
        # get product name with `text`
        response = requests.get(CHAINMART_BE + "/api/products/search/" + keyword).json()

        if len(response) == 0:
            return dict(
                type="text", text="Xin lỗi, chúng tôi không tìm thấy sản phẩm này."
            )

        # result = executeQueryMongo(query, "products")

        # if result is None:
        #     print('Result is None')
        #     return ["Xin lỗi, chúng tôi không tìm thấy sản phẩm này."]

        # result_nraw = []
        # for r in result:
        #     result_nraw.append(
        #         "Sản phẩm {name} có giá là {price}.".format(name=r[0], price=r[1])
        #     )

        # print('Result after query: ', result_nraw)

        # return result_nraw
        result = []
        for r in response:
            result.append(
                dict(
                    name=r["name"],
                    price=r["price"],
                    slug=r["slug"],
                    sale=r["sale"],
                    image=r["images"][0],
                )
            )

        return dict(type="search_product", products=result)

    if action == "action_cung_cap_sdt_tra_cuu_don_hang":
        # get order with `text`
        response = requests.get(CHAINMART_BE + "/api/orders/search/" + keyword).json()

        # result = executeQueryPostgres(query)

        if len(response) == 0:
            return dict(
                type="text",
                text="Chúng tôi không tìm thấy đơn hàng với số điện thoại " + keyword,
            )

        result = []
        for r in response:
            result.append(
                dict(status=r["status"], total=r["total"], address=r["address"])
            )

        return dict(type="search_orders", orders=result)

    if action == "action_provide_product_name":
        # if action == "action_cung_cap_ten_san_pham":
        #     item = unidecode(keyword.strip().lower())
        #     query = { "name" : f"/.*{item}*./"}

        #     print(query)

        #     result = executeQueryMongo(query, "products")

        #     if result is None:
        #         print('Result is None')
        #         return ["Xin lỗi, chúng tôi không tìm thấy sản phẩm này."]

        #     result_nraw = []
        #     for r in result:
        #         result_nraw.append(
        #             "Sản phẩm {name} có giá là {price}.".format(name=r[0], price=r[1])
        #         )

        #     print('Result after query: ', result_nraw)

        #     return result_nraw
        # get product name with `text`
        response = requests.get(CHAINMART_BE + "/api/products/search/" + keyword).json()

        if len(response) == 0:
            return dict(
                type="text", text="Xin lỗi, chúng tôi không tìm thấy sản phẩm này."
            )

        result = []
        for r in response:
            result.append(
                dict(
                    name=r["name"],
                    price=r["price"],
                    slug=r["slug"],
                    sale=r["sale"],
                    image=r["images"][0],
                )
            )

        return dict(type="search_product", products=result)

    if action == "action_provide_phone_number_to_check_order":
        # get order with `text`
        response = requests.get(CHAINMART_BE + "/api/orders/search/" + keyword).json()

        # result = executeQueryPostgres(query)
        if len(response) == 0:
            return dict(
                type="text",
                text="Chúng tôi không tìm thấy đơn hàng với số điện thoại " + keyword,
            )

        result = []
        for r in response:
            result.append(
                dict(status=r["status"], total=r["total"], address=r["address"])
            )

        return dict(type="search_orders", orders=result)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def send(sid, data):
    print("send ", sid)
    print("message ", data)
    response = requests.post(
        RASA_SERVER,
        json={"sender": sid, "message": data},
    ).json()

    if len(response) == 0:
        sio.emit(
            "receive",
            dict(
                type="text",
                text="Xin lỗi, chúng tôi không hiểu yêu cầu của bạn. Vui lòng liên hệ 0984526014 để gặp tư vấn viên.",
            ),
            room=sid,
        )
        return

    text = response[0]["text"]

    if "|" in text:
        res = processMessage(text)

        await sio.emit("receive", res, room=sid)

    else:
        await sio.emit("receive", dict(type="text", text=text), room=sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    web.run_app(app, port=5000)
