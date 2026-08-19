
class User:
    def __init__ (self, name: str, last_name: str, email: str, phone: str, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password

        user = {"name": name, "last_name": last_name, "email": email, "phone": phone, "password": password}
