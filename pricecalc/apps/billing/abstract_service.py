import abc


class Billing(abc.ABC):
    @abc.abstractmethod
    def create_new_payment(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def check_webhook_info(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create_new_customer(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create_subscription(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def send_receipt_to_email(self, *args, **kwargs):
        pass
