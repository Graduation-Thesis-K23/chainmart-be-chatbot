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
