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


        print(sender_id)
        print(so_don_hang)
        
        dispatcher.utter_message(text="Đơn hàng của bạn đang được vận chuyển 1 2")

        return []
