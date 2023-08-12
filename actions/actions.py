from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class CungCapTenSanPham(Action):
    def name(self) -> Text:
        return "action_cung_cap_ten_san_pham"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ten_san_pham = tracker.get_slot("ten_san_pham")

        print("action_cung_cap_ten_san_pham")

        if (ten_san_pham is None):
            return []
        
        print("ten_san_pham" + ten_san_pham)

        dispatcher.utter_message(
            text=f"action_cung_cap_ten_san_pham|{ten_san_pham}".format(
                ten_san_pham=ten_san_pham,
            )
        )

        return []


class ProvideProductName(Action):
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
        print("action_provide_product_name")

        if (ten_san_pham is None):
            return []
        

        print("ten_san_pham" + ten_san_pham)

        dispatcher.utter_message(
            text=f"action_provide_product_name|{ten_san_pham}".format(
                ten_san_pham=ten_san_pham,
            )
        )

        return []


class CungCapSdtTraCuuDonHang(Action):
    def name(self) -> Text:
        return "action_cung_cap_sdt_tra_cuu_don_hang"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        phone_number = tracker.get_slot("phone_number")

        print("action_cung_cap_sdt_tra_cuu_don_hang")

        if (phone_number is None):
            return []
        

        print("phone_number" + phone_number)

        dispatcher.utter_message(
            text=f"action_cung_cap_sdt_tra_cuu_don_hang|{phone_number}".format(
                phone_number=phone_number
            )
        )

        return []


class ProvidePhoneNumberToCheckOrder(Action):
    def name(self) -> Text:
        return "action_provide_phone_number_to_check_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        phone_number = tracker.get_slot("phone_number")

        print("action_provide_phone_number_to_check_order")

        if (phone_number is None):
            return []
        

        print("phone_number" + phone_number)
        dispatcher.utter_message(
            text=f"action_provide_phone_number_to_check_order|{phone_number} ".format(
                phone_number
            )
        )

        return []
