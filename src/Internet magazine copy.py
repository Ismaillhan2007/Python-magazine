class UserExistError(Exception):
    def __str__(self):
         return 'Пользователь уже существует'

class UserNotFoundError(Exception):
    def __str__(self):
         return 'Пользователь не найден'

class UserPasswordError(Exception):
     def __str__(self):
         return 'Неправильный пароль'

class ProductNotFoundError(Exception):
    def __str__(self):
        return 'Продукт не найден'

class InsufficientQuantityError(Exception):
    def __str__(self):
        return 'Недостаточно продуктов'

class Shop:
    def __init__(self):
        self.products = {}
        self.load_products()
    
    def load_products(self):
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    product, quantity, price = line.strip().split(',')
                    self.products[product] = {'quantity': int(quantity), 'price': float(price)}
        except FileNotFoundError:
            self.products = {int(input())}
            self.save_products()
    
    def save_products(self):
        with open('products.txt', 'w') as file:
            for product, details in self.products.items():
                file.write(f"{product},{details['quantity']},{details['price']}\n")

class User:
    def __init__(self, name, age, isadmin=False):
        self.name = name
        self.age = age
        self.users = {}
        self.isadmin = isadmin
        self.cart = {}
        self.load_users()
    
    def load_users(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    user_id, username, password, isadmin = line.strip().split(',')
                    self.users[int(user_id)] = {
                        'username': username,
                        'password': password,
                        'isadmin': isadmin == 'True'
                    }
        except FileNotFoundError:
            pass

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user_id, data in self.users.items():
                file.write(f"{user_id},{data['username']},{data['password']},{data['isadmin']}\n")

    def register(self, username, password):
        if any(user['username'] == username for user in self.users.values()):
            raise UserExistError
        user_id = len(self.users) + 1
        self.users[user_id] = {'username': username, 'password': password}
        print(f'Successfully registered. Your ID: {user_id}')
        self.login_flow(user_id)
    def register_as_admin(self,username,password,isadmin = True):
        self.register(username, password, isadmin)
        self.isadmin = True
            
        
    

    def login(self, name, password):
        for user_id, data in self.users.items():
            if data['name'] == name:
                if data['password'] == password:
                    print(f'Successfully logged in. Welcome, {name}!')
                    self.login_flow(user_id)
                    return
                else:
                    raise UserPasswordError
        raise UserNotFoundError
    def login_as_admin(self, name, password):
        for user_id,data in self.users.items():
            if data['name'] == name:
                if data['password'] == password:
                    print(f'Successfully logged in. Welcome, {name}!')
                    self.login_flow(user_id)
                    self.isadmin = True
                    return
                else:
                    raise UserPasswordError

    def login_flow(self, user_id):
        self.current_user = user_id
        while True:
            print('\n1. Change password')
            print('2. View products')
            if self.isadmin:
                print('3. Add product')
                print('4. Update product')
                print('5. Delete product')
            else:
                print('3. Add to cart')
                print('4. View cart')
                print('5. Checkout')
            print('6. Logout')

            choice = input("Enter the number: ")
            
            if choice == '1':
                new_password = input("Enter new password: ")
                self.users[user_id]['password'] = new_password
                print('Password changed successfully')
            elif choice == '2':
                self.view_products()
            elif choice == '3' and self.isadmin:
                self.add_product()
            elif choice == '3' and not self.isadmin:
                self.add_to_cart()
            elif choice == '4' and self.isadmin:
                self.update_product()
            elif choice == '4' and not self.isadmin:
                self.view_cart()
            elif choice == '5' and self.isadmin:
                self.delete_product()
            elif choice == '5' and not self.isadmin:
                self.checkout()
            elif choice == '6':
                print("Logged out successfully.")
                self.current_user = None
                break
            else:
                print('Invalid choice')

    def view_products(self):
        print("\nAvailable products:")
        for product, details in shop.products.items():
            print(f"{product}: {details['quantity']} in stock, ${details['price']} each")

    def add_product(self):
        product = input("Enter product name: ")
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
        
        if product in shop.products:
            shop.products[product]['quantity'] += quantity
            shop.products[product]['price'] = price
            shop.save_products()
            print(f"Product {product} updated successfully")
        else:
            shop.products[product] = {'quantity': quantity, 'price': price}
            shop.save_products()
            print(f"Product {product} added successfully")

    def update_product(self):
        product = input("Enter product name: ")
        quantity = int(input("Enter new quantity: "))
        price = float(input("Enter new price: "))
        
        if product in shop.products:
            shop.products[product]['quantity'] = quantity
            shop.products[product]['price'] = price
            shop.save_products()
            print(f"Product {product} updated successfully")
        else:
            raise ProductNotFoundError

    def delete_product(self):
        product = input("Enter product name: ")
        
        if product in shop.products:
            del shop.products[product]
            shop.save_products()
            print(f"Product {product} deleted successfully")
        else:
            raise ProductNotFoundError

    def add_to_cart(self):
        product = input("Enter product name: ")
        quantity = int(input("Enter quantity: "))
        
        if product not in shop.products:
            raise ProductNotFoundError
        
        if shop.products[product]['quantity'] < quantity:
            raise InsufficientQuantityError
        
        if product in self.cart:
            self.cart[product] += quantity
        else:
            self.cart[product] = quantity
        
        print(f"Added {quantity} {product}(s) to cart")

    def view_cart(self):
        if not self.cart:
            print("Cart is empty")
            return
            
        total = 0
        print("\nYour cart:")
        for product, quantity in self.cart.items():
            price = shop.products[product]['price'] * quantity
            total += price
            print(f"{product}: {quantity} x ${shop.products[product]['price']} = ${price}")
        print(f"Total: ${total}")

    def checkout(self):
        if not self.cart:
            print("Cart is empty")
            return
            
        for product, quantity in self.cart.items():
            shop.products[product]['quantity'] -= quantity
        
        shop.save_products()
        self.cart = {}
        print("Checkout completed successfully!")

    def get_user_by_id(self, user_id):
        user = self.users.get(user_id)
        if user:
            print(f'User ID {user_id}: Username = {user["username"]}, Password = {user["password"]}')
        else:
            raise UserNotFoundError(f'User with ID {user_id} not found')

    def delete_user(self, user_id):
        if user_id not in self.users:
            raise UserNotFoundError
        username = self.users[user_id]['username']
        del self.users[user_id]
        print(f'User {username} deleted successfully')

def main():
    global manager, shop
    manager = User("Admin")
    shop = Shop()

    
    while True:
        print('\nchoose action')
        print('1. register')
        print('2.register_as_admin')
        print('3. login')
        print('4.login_as_admin')
        print('5.get info by id')
        print('6. delete user')
        print('7. exit\n')

        choice = input('Enter the number: ')

        try:
            if choice == '1':
                username = input('Enter username: ')
                password = input('Enter password: ')
                manager.register(username, password)
            elif choice == '2':
                username = input('Enter username: ')
                password = input('Enter password: ')
                manager.register(username, password)
            elif choice == '3':
                username = input('Enter username: ')
                password = input('Enter password: ')
                manager.login(username, password)
            elif choice == '4':
                user_id = int(input('Enter user ID: '))
                manager.login(user_id)
            elif choice == '5':
                user_id = int(input('Enter user ID: '))
                manager.get_user_by_id(user_id)
            elif choice == '6':                                             
                user_id = int(input('Enter user ID: '))
                manager.delete_user(user_id)
            elif choice == '7':
                print('Program ending')
                break
            else:
                print('Invalid choice, try again')

        except (UserExistError, UserNotFoundError, UserPasswordError) as e:
            print(f'Error: {e}')
        except ValueError:
            print('Invalid input. Please try again')



