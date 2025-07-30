import csv
import random
from faker import Faker
from datetime import datetime
import uuid

fake = Faker()

NUM_CUSTOMERS = 100
NUM_PRODUCTS = 50
NUM_ORDERS = 200

def generate_customers(num_customers):
    customers = []
    with open('customers.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CustomerID', 'Name', 'Email', 'Phone', 'Address'])
        for i in range(1, num_customers + 1):
            writer.writerow([
                i,
                fake.name(),
                fake.email(),
                fake.phone_number(),
                fake.address().replace('\n', ', ')
            ])
            customers.append(i)
    return customers

def generate_products(num_products):
    products = []
    product_names = [
        "Wireless Mouse", "Bluetooth Speaker", "Running Shoes", "Smart Watch", "Coffee Maker",
        "LED Monitor", "Desk Lamp", "Laptop Stand", "USB-C Charger", "Noise Cancelling Headphones",
        "Fitness Tracker", "Backpack", "Electric Toothbrush", "Hair Dryer", "Water Bottle"
    ]
    
    product_categories = [
        "Electronics", "Fitness", "Home", "Appliances", "Accessories", "Office", "Health", "Travel"
    ]

    with open('products.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ProductID', 'Name', 'Category', 'Price'])
        for i in range(1, num_products + 1):
            name = random.choice(product_names)
            category = random.choice(product_categories)
            price = round(random.uniform(10.0, 300.0), 2)
            writer.writerow([i, name, category, price])
            products.append(i)
    return products

def generate_orders(num_orders, customers, products):
    with open('orders.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'OrderID', 'CustomerID', 'ProductID', 'OrderDate', 'Quantity', 'Price'
        ])
        for _ in range(num_orders):
            writer.writerow([
                str(uuid.uuid4()),
                random.choice(customers),
                random.choice(products),
                fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
                random.randint(1, 5),
                round(random.uniform(10.0, 100.0), 2)
            ])

if __name__ == '__main__':
    customers = generate_customers(NUM_CUSTOMERS)
    products = generate_products(NUM_PRODUCTS)
    generate_orders(NUM_ORDERS, customers, products)
    print("✅ Data files generated.")
