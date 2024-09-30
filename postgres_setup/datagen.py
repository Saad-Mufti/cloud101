import csv
import random
from datetime import datetime

# Replace with your actual Google Cloud Storage bucket name
BUCKET_NAME = "mtc-cloud101-cars"

# Lists for generating random data
makes_and_models = {
    'Toyota': ['Camry', 'Corolla', 'Rav4', 'Highlander', 'Tacoma'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey'],
    'Ford': ['F-150', 'Escape', 'Explorer', 'Mustang', 'Focus'],
    'Chevrolet': ['Silverado', 'Equinox', 'Malibu', 'Traverse', 'Camaro'],
    'Nissan': ['Altima', 'Rogue', 'Sentra', 'Murano', 'Pathfinder'],
    'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'GLC', 'GLE', 'S-Class'],
    'Audi': ['A4', 'Q5', 'A6', 'Q7', 'A3'],
    'Volkswagen': ['Jetta', 'Passat', 'Tiguan', 'Atlas', 'Golf'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona']
}
fuel_types = ['Gasoline', 'Diesel', 'Electric', 'Hybrid']

# Generate correct GCP Storage URLs for each make/model
image_urls = {}
for make, models in makes_and_models.items():
    for model in models:
        # Generate the correct GCP Storage URL for each make/model
        image_urls[f"{make}_{model}"] = f"https://storage.googleapis.com/{BUCKET_NAME}/{make}_{model}.jpg"

# Function to generate a random car entry
def generate_car():
    make = random.choice(list(makes_and_models.keys()))
    model = random.choice(makes_and_models[make])
    year = random.randint(2010, datetime.now().year)
    mileage = random.randint(0, 150000)
    fuel_type = random.choice(fuel_types)
    cost = random.randint(5000, 100000)
    image_url = image_urls[f"{make}_{model}"]
    
    return [cost, year, make, model, mileage, fuel_type, image_url]

# Generate 1000 car entries
cars = [generate_car() for _ in range(1000)]

# Write to CSV file
with open('car_inventory.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Cost', 'Year', 'Make', 'Model', 'Mileage', 'Fuel Type', 'Image URL'])
    writer.writerows(cars)

print("Generated 1000 car entries and saved to car_inventory.csv")

# Generate a separate CSV for unique make/model combinations with image URLs
unique_combinations = set((make, model) for _, _, make, model, _, _, _ in cars)
with open('car_images.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Make', 'Model', 'Image URL'])
    for make, model in unique_combinations:
        writer.writerow([make, model, image_urls[f"{make}_{model}"]])

print("Generated unique make/model combinations with image URLs and saved to car_images.csv")