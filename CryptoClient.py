class CryptoClient(object):
    def get_amount_invested(self):
        raise NotImplementedError

    def get_current_value(self):
        raise NotImplementedError

    def get_current_state(self):
        amount_invested = self.get_amount_invested()
        current_value = self.get_current_value()
        return current_value, amount_invested
