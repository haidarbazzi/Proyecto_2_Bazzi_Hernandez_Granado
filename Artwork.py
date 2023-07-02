class Artwork ():
    def __init__(self, code, name, price, year, status, delete):
           self.code = code
           self.name = name
           self.price = price
           self.year = year
           self.status = status
           self.delete = delete

    def show_attr(self):
        return f"Cota: {self.code}\nNombre: {self.name}\nPrice: {self.price}\nAño: {self.year}\nStatus: {self.status}"