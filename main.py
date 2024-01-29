from datetime import datetime, timedelta

class Menu:
    def __init__(self):
        self.menu = {
            1: {"name": "Plov", "price": 10, "description": "Signature Uzbek dish with rice, meat, carrots, onions, and spices."},
            2: {"name": "Manti", "price": 12, "description": "Steamed dumplings with minced meat, onions, and spices."},
            3: {"name": "Shashlik", "price": 15, "description": "Skewered and grilled chunks of marinated meat."},
            4: {"name": "Lagman", "price": 11, "description": "Noodle soup with savory broth, meat, vegetables, and spices."},
            5: {"name": "Samsa", "price": 8, "description": "Savory pastry filled with minced meat, onions, and spices."},
            6: {"name": "Shurpa", "price": 9, "description": "Traditional soup with meat, vegetables, and aromatic herbs."},
            7: {"name": "Non", "price": 5, "description": "Flatbread, a staple in Uzbek cuisine."},
            8: {"name": "Chuchvara", "price": 10, "description": "Small dumplings filled with minced meat, onions, and spices."},
            9: {"name": "Achichuk Salad", "price": 7, "description": "Refreshing salad with tomatoes, cucumbers, onions, and herbs."},
            10: {"name": "Kazan Kebab", "price": 14, "description": "Slow-cooked dish with meat, potatoes, carrots, and spices."},
        }

    def add_item(self, name, price, description):
        item_id = max(self.menu.keys(), default=0) + 1
        self.menu[item_id] = {"name": name, "price": price, "description": description}
        print(f"Item added to menu: {name} - ${price}")

    def remove_item(self, item_id):
        if item_id in self.menu:
            removed_item = self.menu.pop(item_id)
            print(f"Item removed from menu: {removed_item['name']} - ${removed_item['price']}")
        else:
            print("Invalid item ID. Please try again.")

    def update_item(self, item_id, name, price, description):
        if item_id in self.menu:
            self.menu[item_id] = {"name": name, "price": price, "description": description}
            print(f"Menu updated for item ID {item_id}: {name} - ${price}")
        else:
            print("Invalid item ID. Please try again.")

    def display_menu(self):
        print("\nMenu:")
        print("{:<5} {:<20} {:<10} {}".format("ID", "Name", "Price", "Description"))
        print("-" * 50)

        for item_id, item in self.menu.items():
            print("{:<5} {:<20} ${:<10} {}".format(item_id, item['name'], item['price'], item['description']))


class Reservation:
    def __init__(self, name, table_number, order, start_time, duration):
        self.name = name
        self.table_number = table_number
        self.order = order
        self.start_time = start_time
        self.duration = duration
        self.item = Menu()

    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def overlaps_with(self, other_reservation):
        return (self.start_time < other_reservation.end_time() and
                other_reservation.start_time < self.end_time())


    def calculate_total_price(self):
        total_price = 0
        for item_id in self.order:
            total_price += self.item.menu[item_id]['price']
        return total_price

    def __str__(self):
        order_str = ", ".join(str(self.item.menu[item_id]['name']) for item_id in self.order)
        total_price = self.calculate_total_price()
        return f"Name: {self.name}\nTable Number: {self.table_number}\nOrder: {order_str}\nTotal Price: ${total_price:.2f}"






class Manager:
    def __init__(self):
        self.item = Menu()
        self.admin_username = "admin"
        self.admin_password = "admin"
        self.logged_in_as_staff = False
        self.reservations = {}
        self.table_availability = {table_num: [] for table_num in range(1, 21)}

    def customer_menu(self):
        name = input("Enter your name: ")
        print(f'We are glad to see you in our restaurant, {name}')

        while True:
            table_number = self.get_available_table()
            if table_number:
                break

        customer_order = []
        start_time = self.get_reservation_start_time()

        while True:
            print("\nCustomer Menu:")
            print("1. View Menu")
            print("2. Make a Reservation")
            print("3. View Your Reservations")
            print("4. Update Your Reservation")
            print("5. Cancel Your Reservation")
            print("6. About our restaurant")
            print("0. Finish")

            choice = input("Enter your choice: ")

            if choice == '0':
                break
            elif choice == '1':
                self.item.display_menu()
            elif choice == '2':
                if start_time:
                    while True:
                        self.item.display_menu()
                        meal_id = input("\nEnter the ID of the meal you want to order (0 to finish): ")
                        if meal_id == '0':
                            break
                        meal_id = int(meal_id)
                        if meal_id in self.item.menu:
                            customer_order.append(meal_id)
                        else:
                            print("Invalid meal ID. Please try again.")
                        if len(customer_order) >= 10:
                            print("You can only order a maximum of 10 meals.")
                            break

                    duration = int(input("Enter the duration of the reservation in minutes: "))

                    new_reservation = Reservation(name, table_number, customer_order, start_time, duration)
                    if not self.check_reservation_conflicts(new_reservation):
                        self.add_reservation(new_reservation)
                        print("Reservation successful.")
                    else:
                        print("Reservation could not be made due to timing conflicts.")

            elif choice == '3':
                self.view_customer_reservations(name)
            elif choice == '4':
                self.update_customer_reservation(name)
            elif choice == '5':
                self.cancel_customer_reservation(name)
            elif choice == '6':
                self.about_restaurant()
            else:
                print("Invalid choice. Please try again.")


    def get_available_table(self):
        available_tables = [table_num for table_num, slots in self.table_availability.items() if not slots]
        if available_tables:
            table_number = available_tables[0]
            print(f"Table {table_number} is available.")
            return table_number
        else:
            print("Sorry, no tables are currently available.")
            return None

    def get_reservation_start_time(self):
        while True:
            start_time_str = input("Enter the reservation start time (hours:minutes): ")
            try:
                default_date = datetime.now().strftime("%Y-%m-%d")
                start_time = datetime.strptime(f"{default_date} {start_time_str}", "%Y-%m-%d %H:%M")
                print("Current time:", datetime.now())
                print("Entered time:", start_time)
                if start_time <= datetime.now():
                    print("Reservation time should be in the future.")
                else:
                    return start_time
            except ValueError:
                print("Invalid time format. Please enter time in HH:MM format.")

    def add_reservation(self, reservation):
        self.reservations[reservation.name] = reservation
        end_time = reservation.end_time()
        self.table_availability[reservation.table_number].append((reservation.start_time, end_time))

    def check_reservation_conflicts(self, new_reservation):
        existing_slots = self.table_availability.get(new_reservation.table_number, [])
        for slot in existing_slots:
            if new_reservation.start_time < slot[1] and new_reservation.end_time() > slot[0]:
                print("There is a timing conflict with an existing reservation.")
                return True
        return False

    def view_customer_reservations(self, customer_name):
        print(f"\nReservations for {customer_name}:")
        for reservation in self.reservations:
            if reservation.name == customer_name:
                order_items = [str(self.item.menu[item_id]['name']) for item_id in reservation.order]
                order_str = ', '.join(order_items)
                total_price = reservation.calculate_total_price()
                print(f"Table: {reservation.table_number}, Order: {order_str}, Total Price: ${total_price:.2f}")

    def update_customer_reservation(self, customer_name):
        print(f"\nUpdating reservation for {customer_name}:")
        for i, reservation in enumerate(self.reservations):
            if reservation.name == customer_name:
                print(f"Reservation {i + 1}:")
                print(reservation)

                while True:
                    self.item.display_menu()
                    meal_id = input("\nEnter the ID of the meal you want to add (0 to finish): ")
                    if meal_id == '0':
                        break
                    meal_id = int(meal_id)
                    if meal_id in self.item.menu:
                        reservation.order.append(meal_id)
                        print(f"{self.item.menu[meal_id]['name']} added to the order.")
                    else:
                        print("Invalid meal ID. Please try again.")

                    if len(reservation.order) >= 10:
                        print("You can only order a maximum of 10 meals.")
                        break

                print("Reservation updated successfully:")
                print(reservation)
                break
        else:
            print("No reservations found for the specified customer.")

    def cancel_customer_reservation(self, customer_name):
        print(f"\nCanceling reservation for {customer_name}:")
        for i, reservation in enumerate(self.reservations):
            if reservation.name == customer_name:
                print(f"Reservation {i + 1}:")
                print(reservation)
                confirm = input("Are you sure you want to cancel this reservation? (yes/no): ")
                if confirm.lower() == 'yes':
                    removed_reservation = self.reservations.pop(i)
                    print(f"Reservation canceled successfully for {customer_name}")
                    break
                else:
                    print("Reservation not canceled.")
                    break
        else:
            print("No reservations found for the specified customer.")

    def about_restaurant(self):
        print("Our restaurant was created in 2023 by Doniyor. Location: Yangi Sergeli near 'Car Bazaar'")

    def staff_menu(self):
        print("Hello, In order to enter the staff system, you should know a special username and password :)")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        print("You successfully logged in as a staff")

        if username == self.admin_username and password == self.admin_password:
            self.logged_in_as_staff = True

            while self.logged_in_as_staff:
                print("\nStaff Menu:")
                print("1. View Menu")
                print("2. View Restaurant Details")
                print("3. View Reservation Details for All Customers")
                print("4. View Reservation Details for a Specific Customer")
                print("5. Update Reservation Details for a Specific Customer")
                print("6. Cancel Reservation for a Specific Customer")
                print("7. Add New Menu Item")
                print("8. Update Menu Item")
                print("9. Delete Menu Item")
                print("10. Logout")

                choice = input("Enter your choice: ")
                if choice == '1':
                    self.item.display_menu()
                elif choice == '2':
                    self.view_restaurant_details()
                elif choice == '3':
                    self.view_all_reservations()
                elif choice == '4':
                    customer_name = input("Enter the customer's name: ")
                    self.view_customer_reservations(customer_name)
                elif choice == '5':
                    customer_name = input("Enter the customer's name: ")
                    self.update_customer_reservation(customer_name)
                elif choice == '6':
                    customer_name = input("Enter the customer's name: ")
                    self.cancel_customer_reservation(customer_name)
                elif choice == '7':
                    self.add_menu_item()
                elif choice == '8':
                    item_id = int(input("Enter the ID of the item to update: "))
                    self.update_menu_item(item_id)
                elif choice == '9':
                    item_id = int(input("Enter the ID of the item to delete: "))
                    self.delete_menu_item(item_id)
                elif choice == '10':
                    self.logged_in_as_staff = False
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid login or password.")

    def view_restaurant_details(self):
        print("Our restaurant was created in 2023 by Doniyor. Location: Yangi Sergeli near 'Car Bazaar'")

    def view_all_reservations(self):
        print("\nReservations for All Customers:")
        for reservation in self.reservations:
            self.display_reservation_details(reservation)

    def display_reservation_details(self, reservation):
        order_items = [str(self.item.menu[item_id]['name']) for item_id in reservation.order]
        order_str = ', '.join(order_items)
        total_price = reservation.calculate_total_price()
        print(
            f"Name: {reservation.name}, Table: {reservation.table_number}, Order: {order_str}, Total Price: ${total_price:.2f}")

    def add_menu_item(self):
        name = input("Enter the name of the new item: ")
        price = float(input("Enter the price of the new item: "))
        description = input("Enter the description of the new item: ")
        self.item.add_item(name, price, description)

    def update_menu_item(self, item_id):
        if item_id in self.item.menu:
            name = input("Enter the new name of the item: ")
            price = float(input("Enter the new price of the item: "))
            description = input("Enter the new description of the item: ")
            self.item.update_item(item_id, name, price, description)
        else:
            print("Invalid item ID please try again.")

    def delete_menu_item(self, item_id):
        if item_id in self.item.menu:
            self.item.remove_item(item_id)
        else:
            print("Invalid item id please try again.")


if __name__ == "__main__":
    system = Manager()

    while True:
        print("\nMain Menu:")
        print("1. Customer")
        print("2. Staff")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            system.customer_menu()
        elif choice == '2':
            system.staff_menu()
        elif choice == '3':
            break
        else:
            print("Invalid choice try again.")










