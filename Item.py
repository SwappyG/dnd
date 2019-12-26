class Item(object):
    def __init__(self, name, description, quantity):
        self._name = name
        self._description = description
        self._quantity = quantity

    def GetName(self):
        return self._name

    def GetDescription(self):
        return self._description

    def GetQuantity(self):
        return self._quantity

    def AddQuantity(self, val):
        if (val < 0):
            return False
        
        self._quantity += val
        return True

    def SetQuantity(self, val):
        if val < 0:
            return False

        self._quantity = val
        return True

    def RemoveQuantity(self, val):
        if val < 0:
            return False
        
        self._quantity = max(0, self._quantity - val)
        return True