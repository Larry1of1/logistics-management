#Logistics and Delivery Management System
#Build a program that helps a delivery company manage customer orders, assign deliveries to riders, track delivery progress, and monitor delivery performance.
#1. Create a function that registers customer orders with an order ID, customer name, delivery address, package description, delivery fee, and order date.
#2. Create a function that registers delivery riders and assigns each rider a unique rider ID.
#3. Create a function that assigns pending orders to available riders and prevents the same order from being assigned to multiple riders.
#4. Create a function that updates delivery statuses, such as Pending, Assigned, In Transit, Delivered, and Failed.
#5. Create a function that generates a Delivery Performance Report showing total orders, successful deliveries, failed deliveries, and delivery success rate.
#6. Create a function that generates a Rider Performance Report ranking riders by completed deliveries, failed deliveries, and total delivery fees earned.
#7. Create a function that generates a Delayed Delivery Report identifying orders that have not been delivered within the expected delivery period.
#8. Create a function that generates a Daily Operations Report showing orders received, deliveries completed, pending deliveries, and delivery revenue for a selected date.
#9. Create a function that saves all order, rider, and delivery records to files so that the information remains available when the program is reopened. [You can try storing the data in json format that should be automatically loaded when the project runs].





# Here, we are importing tools that help us save and load data,
# check if files exist, and work with dates and time.

import json
import os
from datetime import date, datetime




# ==========================================================
# 1.TO STORE ALL FILE NAMES AND DATA STORAGE
# ==========================================================


# Here, we are creating names for the three files where our data
# will be stored and creating empty lists to hold orders, riders,
# and delivery records while the program is running.

ORDERS_FILE = "orders.json"
RIDERS_FILE = "riders.json"
DELIVERIES_FILE = "deliveries.json"

orders = []
riders = []
deliveries = []



# Here, we are creating a list of all the possible stages an order
# can pass through, from waiting for a rider to being delivered
# successfully or failing.

ORDER_STATUSES = [
    "Pending",
    "Assigned",
    "In Transit",
    "Delivered",
    "Failed"
]


# ==========================================================
# 2. SAVE ALL DATA TO JSON FILES
# ==========================================================

# Here, we are taking all the orders, riders, and delivery records
# currently stored in our lists and saving them inside their
# respective JSON files so that the information is not lost
# when the program is closed.

def save_data():
    """Save orders, riders, and delivery records to JSON files."""
    try:
        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4)

        with open(RIDERS_FILE, "w", encoding="utf-8") as file:
            json.dump(riders, file, indent=4)

        with open(DELIVERIES_FILE, "w", encoding="utf-8") as file:
            json.dump(deliveries, file, indent=4)

    except (OSError, TypeError) as error:
        print(f"Error saving data: {error}")


# ==========================================================
# 3. LOAD SAVED DATA WHEN THE PROGRAM STARTS
# ==========================================================
# Here, we are checking if our JSON files already exist and
# bringing back the previously saved orders, riders, and delivery
# records whenever the program starts, so we can continue
# working with the old information instead of starting afresh.



def load_data():
    """Load saved records from JSON files."""
    global orders, riders, deliveries

    loaded_data = {}

    files = {
        "orders": ORDERS_FILE,
        "riders": RIDERS_FILE,
        "deliveries": DELIVERIES_FILE
    }

    try:
        for key, filename in files.items():
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    loaded_data[key] = json.load(file)
            else:
                loaded_data[key] = []

            if not isinstance(loaded_data[key], list):
                raise ValueError(
                    f"{filename} must contain a JSON list."
                )

        # Replace in-memory records only after all files load.
        orders = loaded_data["orders"]
        riders = loaded_data["riders"]
        deliveries = loaded_data["deliveries"]

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error loading data: {error}")
        print("The program will continue with empty records.")

        orders = []
        riders = []
        deliveries = []


# ==========================================================
# 4. HELPER FUNCTIONS
# ==========================================================
# Here, we are making sure the user does not leave an important
# text field empty. If they enter nothing, we ask them to try again.

def get_non_empty_input(prompt):
    """Ask for text that must not be empty."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty. Please try again.")




# Here, we are collecting the delivery fee from the user and
# making sure they enter a valid number that is not negative.

def get_positive_fee(prompt):
    """Accept a valid, non-negative delivery fee."""
    while True:
        try:
            fee = float(input(prompt))

            if fee < 0:
                print("The fee cannot be negative.")
                continue

            return round(fee, 2)

        except ValueError:
            print("Please enter a valid number, for example 1500.")



# Here, we are collecting dates from the user and checking that
# they follow the correct date format. We can also automatically
# use today's date if the user leaves the date empty.

def get_date_input(prompt, default_today=False):
    """Accept a date in YYYY-MM-DD format."""
    while True:
        value = input(prompt).strip()

        if not value and default_today:
            return date.today().isoformat()

        try:
            parsed_date = date.fromisoformat(value)
            return parsed_date.isoformat()

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-10-22.")



# Here, we are searching through all registered orders to find
# an order with the ID entered by the user. If we find it, we
# return the order; otherwise, we return None.

def find_order(order_id):
    """Find an order by its ID."""
    for order in orders:
        if order["order_id"].lower() == order_id.lower():
            return order

    return None


# Here, we are searching through all registered riders to find
# the rider with the ID entered by the user. If we find the rider,
# we return their information; otherwise, we return None.

def find_rider(rider_id):
    """Find a rider by their ID."""
    for rider in riders:
        if rider["rider_id"].lower() == rider_id.lower():
            return rider

    return None


# Here, we are going through all registered riders and counting
# only the riders whose current status is Available. This helps
# us know how many riders are free to receive new deliveries.

def get_available_rider_count():
    """Count riders who are currently available."""
  
    total_available_riders = 0
    for rider in riders:
        if rider['status'] == 'Available':
            total_available_riders += 1

    return total_available_riders




# Here, we are displaying all the important information about
# a particular order, including the customer details, package,
# delivery fee, dates, assigned rider, and current status.

def display_order(order):
    """Display the details of one order."""
    print("-" * 50)
    print(f"Order ID: {order['order_id']}")
    print(f"Customer: {order['customer_name']}")
    print(f"Address: {order['delivery_address']}")
    print(f"Package: {order['package_description']}")
    print(f"Delivery fee: {order['delivery_fee']:.2f}")
    print(f"Order date: {order['order_date']}")
    print(f"Expected delivery: {order['expected_delivery_date']}")
    print(f"Rider ID: {order['rider_id'] or 'Not assigned'}")
    print(f"Status: {order['status']}")


# ==========================================================
# 5. REGISTER CUSTOMER ORDERS
# ==========================================================

# Here, we are collecting all the necessary information about
# a customer's order, including their name, address, package
# description, delivery fee, order date, and expected delivery date.

# We first check that the order ID has not already been used.
# We also make sure the information entered is valid and that
# the expected delivery date is not before the order date.

# After collecting everything, we put the information into a
# dictionary, add that dictionary to our orders list, save the
# information, and display the newly registered order.

def register_order():
    """Register a new customer order."""
    print("\n--- REGISTER CUSTOMER ORDER ---")

    order_id = get_non_empty_input("Enter order ID: ")

    if find_order(order_id):
        print("That order ID already exists.")
        return

    customer_name = get_non_empty_input("Enter customer name: ")
    delivery_address = get_non_empty_input("Enter delivery address: ")
    package_description = get_non_empty_input("Describe the package: ")
    delivery_fee = get_positive_fee("Enter delivery fee: ")

    order_date = get_date_input(
        "Enter order date (YYYY-MM-DD), or press Enter for today: ",
        default_today=True
    )

    while True:
        expected_date = get_date_input(
            "Enter expected delivery date (YYYY-MM-DD): "
        )

        if expected_date < order_date:
            print("Expected delivery cannot be before the order date.")
        else:
            break

    order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "delivery_address": delivery_address,
        "package_description": package_description,
        "delivery_fee": delivery_fee,
        "order_date": order_date,
        "expected_delivery_date": expected_date,
        "rider_id": None,
        "status": "Pending",
        "completed_date": None
    }

    orders.append(order)
    save_data()

    print("Order registered successfully!")
    display_order(order)


# ==========================================================
# 6. REGISTER DELIVERY RIDERS
# ==========================================================

# Here, we are collecting the rider's unique ID and name.
# We first check that the rider ID has not already been registered.

# After that, we create a dictionary containing the rider's ID,
# name, and availability status. We automatically make every
# newly registered rider Available, add them to our riders list,
# and save their information.

def register_rider():
    """Register a new delivery rider."""
    print("\n--- REGISTER DELIVERY RIDER ---")

    rider_id = get_non_empty_input("Enter unique rider ID: ")

    if find_rider(rider_id):
        print("That rider ID already exists.")
        return

    rider_name = get_non_empty_input("Enter rider name: ")

    rider = {
        "rider_id": rider_id,
        "rider_name": rider_name,
        "status": "Available"
    }

    riders.append(rider)
    save_data()

    print("Rider registered successfully!")
    print(f"Rider ID: {rider_id}")
    print(f"Rider name: {rider_name}")
    print("Rider status: Available")


# ==========================================================
# 7. ASSIGN AN ORDER TO AN AVAILABLE RIDER
# ==========================================================

# Here, we are collecting an order ID and checking if the order
# exists and is still Pending.

# We then check if there is at least one available rider.
# After that, we collect the rider ID and confirm that the rider
# exists and is Available.

# Once all the checks are successful, we connect the rider to
# the order, change the order status to Assigned, and change
# the rider's status to Busy.

# We also create a delivery record to keep track of the order,
# the rider assigned to it, the assignment date, and its
# delivery status history.

# Finally, we save all the changes.

def assign_order():
    """Assign one pending order to one available rider."""
    print("\n--- ASSIGN ORDER TO RIDER ---")

    order_id = get_non_empty_input("Enter order ID: ") 
    order = find_order(order_id)

    if order is None:
        print("Order not found.")
        return

    if order["status"] != "Pending":
        print("Only pending orders can be assigned.")
        return

    if get_available_rider_count() == 0:
        print("No riders are currently available.")
        return

    rider_id = get_non_empty_input("Enter rider ID: ")
    rider = find_rider(rider_id)

    if rider is None:
        print("Rider not found.")
        return

    if rider["status"] != "Available":
        print("This rider is not available.")
        return

    order["rider_id"] = rider["rider_id"]
    order["status"] = "Assigned"
    rider["status"] = "Busy"

    deliveries.append({
        "order_id": order["order_id"],
        "rider_id": rider["rider_id"],
        "assigned_date": date.today().isoformat(),
        "status_history": [
            {
                "status": "Assigned",
                "date": date.today().isoformat()
            }
        ]
    })

    save_data()

    print("Order assigned successfully!")
    print(f"Order {order['order_id']} assigned to {rider['rider_name']}.")


# ==========================================================
# 8. UPDATE DELIVERY STATUS
# ==========================================================


# Here, we are collecting an order ID and checking if the order
# exists and is eligible for a status update.

# We prevent orders that are still Pending from being updated
# and also prevent orders that are already Delivered or Failed
# from being changed again.

# We then display the available delivery statuses and allow
# the user to choose the new status using a number.

# We check that the new status follows the correct delivery
# process. For example, an Assigned order can move to In Transit
# or Failed, while an In Transit order can move to Delivered
# or Failed.

# When an order reaches Delivered or Failed, we record its
# completion date and make its rider Available again.

# We also add the new status and date to the delivery history
# and save all the changes.

def update_delivery_status():
    """Update the status of an assigned delivery."""
    print("\n--- UPDATE DELIVERY STATUS ---")

    order_id = get_non_empty_input("Enter order ID: ")
    order = find_order(order_id)

    if order is None:
        print("Order not found.")
        return

    if order["status"] in ("Delivered", "Failed"):
        print("This delivery is already in a final status.")
        return

    if order["status"] == "Pending":
        print("Assign this order to a rider before updating it.")
        return

    print("Available statuses:")

    for index, status in enumerate(ORDER_STATUSES, start=1):
        print(f"{index}. {status}")

    try:
        choice = int(input("Choose a status number: "))

        if choice < 1 or choice > len(ORDER_STATUSES):
            print("Invalid status choice.")
            return

        new_status = ORDER_STATUSES[choice - 1]

    except ValueError:
        print("Please enter a valid number.")
        return

    current_status = order["status"]

    allowed_transitions = {
        "Assigned": ["In Transit", "Failed"],
        "In Transit": ["Delivered", "Failed"]
    }

    if new_status not in allowed_transitions.get(current_status, []):
        print(
            f"Cannot change status from {current_status} "
            f"to {new_status}."
        )
        return

    order["status"] = new_status

    if new_status in ("Delivered", "Failed"):
        order["completed_date"] = date.today().isoformat()

        rider = find_rider(order["rider_id"])

        if rider:
            rider["status"] = "Available"

    for delivery in reversed(deliveries):
        if delivery["order_id"].lower() == order_id.lower():
            delivery["status_history"].append({
                "status": new_status,
                "date": date.today().isoformat()
            })
            break

    save_data()

    print(f"Delivery status updated to: {new_status}")


# ==========================================================
# 9. DELIVERY PERFORMANCE REPORT
# ==========================================================


# Here, we are calculating the overall performance of the
# delivery company.

# First, we count the total number of registered orders.
# We then go through every order and count how many have been
# successfully Delivered and how many have Failed.

# After that, we calculate the delivery success rate by dividing
# successful deliveries by total orders and multiplying by 100.

# Finally, we display the total orders, successful deliveries,
# failed deliveries, and the company's delivery success rate.

def delivery_performance_report():
    """Show overall company delivery performance."""
    print("\n--- DELIVERY PERFORMANCE REPORT ---")

    total_orders = len(orders)

    successful = 0
    failed = 0
    for order in orders:
        if order['status'] == 'Delivered':
            successful += 1
        elif order['status'] == 'Failed':
            failed += 1


    success_rate = (
        successful / total_orders * 100
        if total_orders > 0 else 0
    )

    print(f"Total orders: {total_orders}")
    print(f"Successful deliveries: {successful}")
    print(f"Failed deliveries: {failed}")
    print(f"Delivery success rate: {success_rate:.2f}%")


# ==========================================================
# 10. RIDER PERFORMANCE REPORT
# ==========================================================


# First, we check if there are any registered riders.
# If there are none, we display a message and stop the function.

# We then create an empty list where we will store the performance
# results of each rider.

# Below, we are taking every rider and calculating how many
# orders are connected to that rider, how many of those orders
# have been completed or failed, and how much the rider has
# earned from the delivered orders connected to them.

# After calculating each rider's performance, we store their
# ID, name, completed deliveries, failed deliveries, and fees
# earned inside a dictionary and add it to our results list.

# We then arrange the riders according to the number of
# successful deliveries, placing the rider with the highest
# number of completed deliveries first.

# Finally, we display the riders in a ranking table showing
# their position, names, completed deliveries, failed deliveries,
# and total delivery fees earned.

def rider_performance_report():
    """Rank riders by deliveries and fees earned."""
    print("\n--- RIDER PERFORMANCE REPORT ---")

    if not riders:
        print("No riders have been registered.")
        return

    rider_results = []

    # Below, we are taking every rider and calculating, how many orders are connected to that rider, how many of the orders he has completed/failed to complete, and how much each of those riders have earned from the [delivered] orders connected to them

    for rider in riders:
        rider_orders = [
            order for order in orders
            if order["rider_id"] == rider["rider_id"]
        ]

        completed = sum(
            1 for order in rider_orders
            if order["status"] == "Delivered"
        )

        failed = sum(
            1 for order in rider_orders
            if order["status"] == "Failed"
        )

        fees_earned = sum(
            order["delivery_fee"] for order in rider_orders
            if order["status"] == "Delivered"
        )

        rider_results.append({
            "rider_id": rider["rider_id"],
            "rider_name": rider["rider_name"],
            "completed": completed,
            "failed": failed,
            "fees_earned": fees_earned
        })


    # Ranking those riders based on their performance that we've calculated above.
    rider_results.sort(
        key=lambda result: result["completed"],
        reverse=True
    )

    print(f"{'Rank':<6}{'Rider':<20}{'Completed':<12}{'Failed':<10}{'Fees Earned':>14}")


    print("-" * 62)

    for rank, result in enumerate(rider_results, start=1):
        print(
            f"{rank:<6}{result['rider_name']:<20}"
            f"{result['completed']:<12}{result['failed']:<10}"
            f"{result['fees_earned']:>14.2f}"
        )


# ==========================================================
# 11. DELAYED DELIVERY REPORT
# ==========================================================

# Here, we are checking all registered orders to identify
# deliveries that have passed their expected delivery dates.

# We first collect today's date and compare it with the expected
# delivery date of every order.

# We only select orders whose expected delivery dates have
# passed and whose statuses are not Delivered or Failed.

# If we find any delayed outstanding orders, we display their
# details. If we find none, we display a message saying there
# are no delayed outstanding deliveries.

def delayed_delivery_report():
    """Identify orders past their expected delivery dates."""
    print("\n--- DELAYED DELIVERY REPORT ---")

    today = date.today().isoformat()

    delayed_orders = [
        order for order in orders
        if order["expected_delivery_date"] < today
        and order["status"] not in ("Delivered", "Failed")
    ]

    if not delayed_orders:
        print("There are no delayed outstanding deliveries.")
        return

    for order in delayed_orders:
        display_order(order)


# ==========================================================
# 12. DAILY OPERATIONS REPORT
# ==========================================================

# Here, we are asking the user to enter a particular date so
# we can generate a report for that selected day.

# We check all the orders and calculate how many orders were
# received on that date, how many deliveries were completed
# on that date, and how many deliveries are currently still
# waiting to be completed.

# We also calculate the total delivery fees earned from
# deliveries completed on the selected date.

# Finally, we display the selected date, orders received,
# deliveries completed, pending deliveries, and total
# delivery revenue.

def daily_operations_report():
    """Show operations and revenue for a selected date."""
    print("\n--- DAILY OPERATIONS REPORT ---")
# We're inputing a specific date and then we get to check how many orders were recieved / completed / pending / and calculating the total sum of the delivry fee for only #that date selected. 
    selected_date = get_date_input(
        "Enter report date (YYYY-MM-DD): "
    )

    received = [
        order for order in orders
        if order["order_date"] == selected_date
    ]

    completed = [
        order for order in orders
        if order["status"] == "Delivered"
        and order["completed_date"] == selected_date
    ]

    pending = [
        order for order in orders
        if order["status"] in ("Pending", "Assigned", "In Transit")
    ]

    revenue = sum(
        order["delivery_fee"] for order in completed
    )

    print(f"Report date: {selected_date}")
    print(f"Orders received: {len(received)}")
    print(f"Deliveries completed on this date: {len(completed)}")
    print(f"Currently pending deliveries: {len(pending)}")
    print(f"Delivery revenue for this date: {revenue:.2f}")


# ==========================================================
# 13. VIEW ALL ORDERS
# ==========================================================

# Here, we are checking if there are any registered customer
# orders. If there are none, we display a message.

# If orders exist, we go through the orders list one by one
# and use our display_order function to show the full details
# of every registered order.

def view_orders():
    """Display all registered orders."""
    print("\n--- ALL CUSTOMER ORDERS ---")

    if not orders:
        print("No orders have been registered.")
        return

    for order in orders:
        display_order(order)


# ==========================================================
# 14. VIEW ALL RIDERS
# ==========================================================

# Here, we are checking if any delivery riders have been
# registered. If there are none, we display a message.

# If riders exist, we go through the riders list one by one
# and display each rider's ID, name, and current availability
# status, showing whether they are Available or Busy.

def view_riders():
    """Display all registered riders."""
    print("\n--- ALL DELIVERY RIDERS ---")

    if not riders:
        print("No riders have been registered.")
        return

    for rider in riders:
        print("-" * 40)
        print(f"Rider ID: {rider['rider_id']}")
        print(f"Rider name: {rider['rider_name']}")
        print(f"Availability: {rider['status']}")


# ==========================================================
# 15. MAIN MENU
# ==========================================================

# Here, we are creating the main function that controls the
# entire program.

# First, we call load_data to bring back previously saved
# information whenever the program starts.

# We then create a continuous loop that keeps displaying
# the main menu and allows the user to choose what they
# want the program to do.

# Depending on the number entered, we call the appropriate
# function to register orders, register riders, assign deliveries,
# update statuses, generate reports, or view records.

# If the user chooses Save Data, we save all the information.
# If the user chooses Exit, we save everything before closing
# the program.

# If the user enters an option that does not exist, we display
# an error message and allow them to try again.


# 
def main():
    """Run the program menu until the user exits."""
    load_data()

    while True:
        print("\n" + "=" * 45)
        print(" LOGISTICS AND DELIVERY MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Register customer order")
        print("2. Register delivery rider")
        print("3. Assign order to rider")
        print("4. Update delivery status")
        print("5. Delivery performance report")
        print("6. Rider performance report")
        print("7. Delayed delivery report")
        print("8. Daily operations report")
        print("9. View all orders")
        print("10. View all riders")
        print("11. Save data")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_order()

        elif choice == "2":
            register_rider()

        elif choice == "3":
            assign_order()

        elif choice == "4":
            update_delivery_status()

        elif choice == "5":
            delivery_performance_report()

        elif choice == "6":
            rider_performance_report()

        elif choice == "7":
            delayed_delivery_report()

        elif choice == "8":
            daily_operations_report()

        elif choice == "9":
            view_orders()

        elif choice == "10":
            view_riders()

        elif choice == "11":
            save_data()
            print("Save operation completed.")

        elif choice == "0":
            save_data()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number from the menu.")


# ==========================================================
# 16. START THE PROGRAM
# ==========================================================

# Here, we are checking if this Python file is being run directly.
# If it is, we call the main function to start the entire
# Logistics and Delivery Management System.

if __name__ == "__main__":
    main()

