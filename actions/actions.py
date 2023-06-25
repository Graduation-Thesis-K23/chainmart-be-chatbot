from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_mood_great"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

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
