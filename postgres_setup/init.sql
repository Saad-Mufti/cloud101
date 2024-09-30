CREATE TABLE IF NOT EXISTS cars (
  id SERIAL PRIMARY KEY,
  make VARCHAR(50) NOT NULL,
  model VARCHAR(50) NOT NULL,
  year INTEGER NOT NULL,
  cost NUMERIC(10, 2) NOT NULL,
  image_url VARCHAR(255),
  mileage INTEGER,
  fuel_type VARCHAR(20)
);
TRUNCATE cars;
INSERT INTO cars (make, model, year, cost, image_url, mileage, fuel_type) VALUES
('Toyota', 'Camry', 2022, 25000, 'https://storage.googleapis.com/mtc-cloud101-cars/Toyota_Camry.jpg', 15000, 'Gasoline'),
('Honda', 'Civic', 2023, 22000, 'https://storage.googleapis.com/mtc-cloud101-cars/Honda_Civic.jpg', 5000, 'Hybrid'),
('Ford', 'Mustang', 2021, 35000, 'https://storage.googleapis.com/mtc-cloud101-cars/Ford_Mustang.jpg', 20000, 'Gasoline'),
('Mercedes-Benz', 'GLC', 2023, 45000, 'https://storage.googleapis.com/mtc-cloud101-cars/Mercedes-Benz_GLC.jpg', 1000, 'Electric'),
('Chevrolet', 'Silverado', 2022, 38000, 'https://storage.googleapis.com/mtc-cloud101-cars/Chevrolet_Silverado.jpg', 18000, 'Diesel');