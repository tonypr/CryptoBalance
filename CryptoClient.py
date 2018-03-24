class CryptoClient(object):
    def get_amount_invested(self):
        raise NotImplementedError

    def get_current_value(self):
        raise NotImplementedError

    def get_current_state(self):
        amount_invested = self.get_amount_invested()
        current_value = self.get_current_value()
        return current_value, amount_invested

    @staticmethod
    def setup_config(cls):
        import inspect

        args = inspect.getargspec(cls.__init__).args[1:]
        arg_config = {arg: "TODO" for arg in args}
        config = {"args": arg_config}

        return config
