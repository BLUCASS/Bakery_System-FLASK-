from database import db
from models import User, Product

class UserManagement:
    
    def signup(self, name, email, password) -> str:
        encrypted_password = self.__make_it_hash(password)
        exists = self.search_email(email)
        if exists:
            return False
        try:
            user = User(name=name, password=encrypted_password, email=email)
            db.session.add(user)
        except:
            db.session.rollback()
        else:
            db.session.commit()
            return user

    def login(self, email, password) -> str:
        encrypted_password = self.__make_it_hash(password)
        user = self.search_email(email)
        if user:
            if user.password == encrypted_password:
                return user
            return False
        
    def delete_user(self, password, confirm_password, user):
        password = self.__make_it_hash(password)
        confirm_password = self.__make_it_hash(confirm_password)
        if password == confirm_password:
            if password == user.password:
                try:
                    db.session.query(User).filter(User.id == user.id).delete()
                except:
                    db.session.rollback()
                    return False
                else:
                    db.session.query(Product).filter(Product.user_id == user.id).delete()
                    db.session.commit()
                    return True
        return False

    def __make_it_hash(self, password) -> str:
        from hashlib import sha256
        password = sha256(password.encode()).hexdigest()
        return password

    def search_email(self, email):
        exists = db.session.query(User).filter(email == email).first()
        return exists
    

class ProductManagement():

    def purchase(self, data, id):
        if int(data["croissant"]) > 0:
            self.__register_product('Croissant', 3, int(data["croissant"]), 3 * int(data["croissant"]), id)
        if int(data["danish"]) > 0:
            self.__register_product('Danish', 2.5, int(data["danish"]), 2.5 * int(data["danish"]), id)
        if int(data["croissandwich"]) > 0:
            self.__register_product('Croissandwich', 3.5, int(data["croissandwich"]), 3.5 * int(data["croissandwich"]), id)
        if int(data["pain"]) > 0:
            self.__register_product('Pain au Chocolat', 3, int(data["pain"]), 3 * int(data["pain"]), id)
        if int(data["choc_swiss"]) > 0:
            self.__register_product('Chocolate Swiss', 4, int(data["choc_swiss"]), 4 * int(data["choc_swiss"]), id)
        if int(data["sausage"]) > 0:
            self.__register_product('Sausage Roll', 3.5, int(data["sausage"]), 3.5 * int(data["sausage"]), id)

    def __register_product(self, name, price, amount, total, user_id):
        user = Product(name=name, price=price, amount=amount, total=total, user_id=user_id)
        try:
            db.session.add(user)
        except:
            db.session.rollback()
        else:
            db.session.commit()

    def get_products(self, id):
        products = db.session.query(Product).filter(Product.user_id == id).all()
        if len(products) == 0:
            return False
        return products

