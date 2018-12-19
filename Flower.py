class Flower:
    def __init__(self, name='daffodil', hbs=5, price=0.00):
        self._name = name
        self._hbs = hbs
        self._price = price

    def get_flowername(self):
        return self._name

    def set_flowername(self, name):
        self._name = name

