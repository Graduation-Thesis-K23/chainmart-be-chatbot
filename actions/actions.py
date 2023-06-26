from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


products = [
    {
        "name": "Nấm bào ngư trắng 300g",
        "price": 14.900,
        "url": "https://www.bachhoaxanh.com/nam-tuoi/nam-bao-ngu-trang-bich-300g",
    },
    {
        "name": "10 gói mì 3 Miền Gold bò hầm rau thơm 75g",
        "price": 50.000,
        "url": "https://www.bachhoaxanh.com/mi/10-goi-mi-3-mien-gold-bo-ham-rau-thom-goi-75g",
    },
    {
        "name": "6 chai nước ngọt Coca Cola 390ml",
        "price": 60.000,
        "url": "https://www.bachhoaxanh.com/nuoc-ngot/6-chai-nuoc-ngot-coca-cola-390ml",
    },
]

orders = [
    {
        "id": "ORDER001",
        "status": "Đang vận chuyển",
    },
    {
        "id": "ORDER002",
        "status": "Đã giao hàng",
    },
    {
        "id": "ORDER003",
        "status": "Đã hủy",
    },
    {
        "id": "ORDER004",
        "status": "Đã giao hàng",
    },
]


class CungCapTenSanPham(Action):
    def name(self) -> Text:
        return "action_cung_cap_ten_san_pham"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # get so_don_hang
        ten_san_pham = tracker.get_slot("ten_san_pham")
        # get name in products like %ten_san_pham%

        result = None
        for product in products:
            if ten_san_pham in product["name"]:
                result = product
                break

        if result is None:
            dispatcher.utter_message(
                text=f"Không tìm thấy sản phẩm {ten_san_pham}".format(ten_san_pham)
            )
        else:
            product_name = result.get("name")
            product_price = result.get("price")
            product_link = result.get("url")

            dispatcher.utter_message(
                text=f"Sản phẩm {product_name} có giá {product_price} VNĐ.\n Link: {product_link}".format(
                    product_name, product_price, product_link
                )
            )

        return []


class CungCapTenSanPham(Action):
    def name(self) -> Text:
        return "action_provide_product_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # get so_don_hang
        ten_san_pham = tracker.get_slot("ten_san_pham")
        # get name in products like %ten_san_pham%

        result = None
        for product in products:
            if ten_san_pham in product["name"]:
                result = product
                break

        if result is None:
            dispatcher.utter_message(
                text=f"{ten_san_pham} not found".format(ten_san_pham)
            )
        else:
            dispatcher.utter_message(
                text=f"{product_name} have price {product_price} VNĐ.\n Link: {product_link}".format(
                    product_name=result.get("name"),
                    product_price=result.get("price"),
                    product_link=result.get("url"),
                )
            )

        return []


class ActionProductDetails(Action):
    def name(self) -> Text:
        return "action_tra_cuu_trang_thai_don_hang"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # get so_don_hang
        so_don_hang = tracker.get_slot("so_don_hang")
        sender_id = tracker.sender_id

        dispatcher.utter_message(
            text=f"Đơn hàng {so_don_hang} của {sender_id} đang được vận chuyển.".format(
                so_don_hang, sender_id
            )
        )

        return []
