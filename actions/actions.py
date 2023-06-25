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
        return "action_product_details"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        product_code = next(tracker.get_latest_entity_values("product_code"), None)

        response = ""

        if product_code:
            product_info = "-Thông tin sản phẩm-"

            response = (
                f"Mã sản phẩm: {product_code}. Thông tin chi tiết: {product_info}"
            )
        else:
            response = "Xin lỗi, tôi không nhận diện được mã sản phẩm."

        dispatcher.utter_message(text=response)

        return []
