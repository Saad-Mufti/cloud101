import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './components/card';
import { Button } from './components/button';
import { Input } from './components/input';
import { Search } from 'lucide-react';
import { Select } from './components/select';

const API_URL = process.env.NODE_ENV == "production" ? "http://34.170.200.38:8080/api" : "http://localhost:5000/api";
console.log("url = " + API_URL)
console.log("env = " + process.env["NODE_ENV"])

const carData = [
  { id: 1, make: 'Toyota', model: 'Camry', year: 2022, cost: 25000, image_url: '/api/placeholder/400/300', mileage: 15000, fuelType: 'Gasoline' },
  { id: 2, make: 'Honda', model: 'Civic', year: 2023, cost: 22000, image_url: '/api/placeholder/400/300', mileage: 5000, fuelType: 'Hybrid' },
  { id: 3, make: 'Ford', model: 'Mustang', year: 2021, cost: 35000, image_url: '/api/placeholder/400/300', mileage: 20000, fuelType: 'Gasoline' },
  { id: 4, make: 'Tesla', model: 'Model 3', year: 2023, cost: 45000, image_url: '/api/placeholder/400/300', mileage: 1000, fuelType: 'Electric' },
  { id: 5, make: 'Chevrolet', model: 'Silverado', year: 2022, cost: 38000, image_url: '/api/placeholder/400/300', mileage: 18000, fuelType: 'Diesel' },
];

const Header = () => (
  <header className="bg-blue-600 text-white p-4">
    <div className="container mx-auto flex justify-between items-center">
      <h1 className="text-2xl font-bold">GCP Motors</h1>
      <nav>
        <ul className="flex space-x-4">
          <li><a href="#" className="hover:underline">Home</a></li>
          <li><a href="#" className="hover:underline">Inventory</a></li>
          <li><a href="#" className="hover:underline">About</a></li>
          <li><a href="#" className="hover:underline">Contact</a></li>
        </ul>
      </nav>
    </div>
  </header>
);

const SearchBar = ({ onSearch }) => (
  <div className="flex w-full max-w-sm items-center space-x-2 mb-4">
    <Input type="text" placeholder="Search cars..." onChange={(e) => onSearch(e.target.value)} />
    <Button type="submit"><Search className="h-4 w-4" /></Button>
  </div>
);

const CarCard = ({ car }) => (
  <Card className="overflow-hidden">
    <img src={car.image_url} alt={`${car.make} ${car.model}`} className="w-full h-48 object-cover" />
    <CardHeader>
      <CardTitle>{car.make} {car.model}</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="font-semibold text-lg">${car.cost.toLocaleString()}</p>
      <p>Year: {car.year}</p>
      <p>Mileage: {car.mileage.toLocaleString()} miles</p>
      <p>Fuel Type: {car.fuel_type}</p>
      <Button className="mt-2 w-full">View Details</Button>
    </CardContent>
  </Card>
);

const CarList = ({ cars }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
    {cars.map((car) => (
      <CarCard key={car.id} car={car} />
    ))}
  </div>
);

const AdvancedSearchForm = ({ onSearch }) => {
  const [filters, setFilters] = useState({
    make: '',
    model: '',
    min_year: '',
    max_year: '',
    min_price: '',
    max_price: '',
    min_mileage: '',
    max_mileage: '',
    fuel_type: '',
  });

  const handleInputChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(filters);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Input
          name="make"
          placeholder="Make"
          value={filters.make}
          onChange={handleInputChange}
        />
        <Input
          name="model"
          placeholder="Model"
          value={filters.model}
          onChange={handleInputChange}
        />
        <Input
          name="min_year"
          type="number"
          placeholder="Min Year"
          value={filters.min_year}
          onChange={handleInputChange}
        />
        <Input
          name="max_year"
          type="number"
          placeholder="Max Year"
          value={filters.max_year}
          onChange={handleInputChange}
        />
        <Input
          name="min_price"
          type="number"
          placeholder="Min Price"
          value={filters.min_price}
          onChange={handleInputChange}
        />
        <Input
          name="max_price"
          type="number"
          placeholder="Max Price"
          value={filters.max_price}
          onChange={handleInputChange}
        />
        <Input
          name="min_mileage"
          type="number"
          placeholder="Min Mileage"
          value={filters.min_mileage}
          onChange={handleInputChange}
        />
        <Input
          name="max_mileage"
          type="number"
          placeholder="Max Mileage"
          value={filters.max_mileage}
          onChange={handleInputChange}
        />
        <Select
          name="fuel_type"
          value={filters.fuel_type}
          onChange={handleInputChange}
        >
          <option value="">Select Fuel Type</option>
          <option value="Gasoline">Gasoline</option>
          <option value="Diesel">Diesel</option>
          <option value="Electric">Electric</option>
          <option value="Hybrid">Hybrid</option>
        </Select>
      </div>
      <Button type="submit" className="w-full">
        <Search className="mr-2 h-4 w-4" /> Search
      </Button>
    </form>
  );
};

const Footer = () => (
  <footer className="bg-gray-200 p-4">
    <div className="container mx-auto text-center">
      <p>&copy; 2024 GCP Motors. All rights reserved.</p>
      <div className="mt-2">
        <a href="#" className="text-blue-600 hover:underline mr-4">Privacy Policy</a>
        <a href="#" className="text-blue-600 hover:underline mr-4">Terms of Service</a>
        <a href="#" className="text-blue-600 hover:underline">Contact Us</a>
      </div>
    </div>
  </footer>
);

const App = () => {
  const [cars, setCars] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCars = async (filters = {}) => {
    setIsLoading(true);
    setError(null);

    const queryParams = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, value);
    });

    try {
      const response = await fetch(`${API_URL}/cars/search?${queryParams}`);
      if (!response.ok) {
        throw new Error('Failed to fetch cars');
      }
      const data = await response.json();
      console.log(data);
      setCars(data);
    } catch (err) {
      console.error('Error fetching cars:', err);
      setError('Failed to fetch cars. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCars();
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow container mx-auto px-4">
        <h2 className="text-2xl font-semibold my-4">Our Inventory</h2>
        <AdvancedSearchForm onSearch={fetchCars} />
        {isLoading ? (
          <p>Loading cars...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <CarList cars={cars} />
        )}
      </main>
      <Footer />
    </div>
  );
};

export default App;