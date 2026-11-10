
import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [cars, setCars] = useState([]);
  const [category, setCategory] = useState('All');
  const [search, setSearch] = useState('');
  const [selectedCar, setSelectedCar] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;

    async function loadCars() {
      try {
        const response = await fetch(
          '/api/companies/2/cars'
        );

        if (!response.ok) {
          throw new Error(
            `Failed to load cars: ${response.status}`
          );
        }

        const data = await response.json();

        if (active) {
          setCars(data);
        }

      } catch (err) {
        if (active) {
          setError(err.message);
        }

      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadCars();

    return () => {
      active = false;
    };
  }, []);


  const filteredCars = cars.filter((car) => {
    const matchesCategory =
      category === 'All' || car.category === category;

    const carName = `${car.brand} ${car.model}`.toLowerCase();

    const matchesSearch =
      carName.includes(search.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  return (
    <>
      <nav className="navbar navbar-dark bg-dark">
        <div className="container">
          <a className="navbar-brand fw-bold" href="/">
            AutoPick
          </a>
          <span className="text-white-50">
            Car Rental
          </span>
        </div>
      </nav>

      <header className="hero">
        <div className="container">
          <h1 className="display-5 fw-bold">
            Find your perfect car
          </h1>
          <p className="lead">
            Choose a car and enjoy a simple rental experience.
          </p>
        </div>
      </header>

      <main className="container py-5">
        <div className="mb-4">
          <h2 className="fw-bold">Available cars</h2>
          <p className="text-muted">
            Browse our vehicle collection.
          </p>
        </div>

        <div className="row g-3 mb-4">
          <div className="col-md-8">
            <input
              type="text"
              className="form-control"
              placeholder="Search by brand or model..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="col-md-4">
            <select
              className="form-select"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option value="All">All categories</option>
              <option value="Economic">Economic</option>
              <option value="Comfort">Comfort</option>
              <option value="Premium">Premium</option>
              <option value="Sport">Sport</option>
            </select>
          </div>
        </div>

        {selectedCar && (
          <div className="alert alert-primary">
            Selected: <strong>
              {selectedCar.brand} {selectedCar.model}
            </strong>
            <div className="small mt-1">
              Booking form will be added in the next step.
            </div>
          </div>
        )}

        <div className="row g-4">
            {loading && (
        <div className="alert alert-info">
                Loading cars...
        </div>
            )}

        {error && (
        <div className="alert alert-danger">
        {error}
        </div>
            )}
          {filteredCars.map((car) => (
            <div className="col-md-6 col-lg-4" key={car.id}>
              <div className="card car-card h-100">
                <div className="car-image">
                  🚘
                </div>

                <div className="card-body">
                  <span className="badge bg-secondary mb-2">
                    {car.category}
                  </span>

                  <h5 className="card-title fw-bold">
                    {car.brand} {car.model}
                  </h5>

                  <p className="text-muted">
                    {car.body_type}
                  </p>

                  <div className="d-flex justify-content-between align-items-center">
                    <div>
                      <span className="fs-4 fw-bold">
                        €{car.base_price}
                      </span>
                      <span className="text-muted"> / day</span>
                    </div>

                    <button
                      className="btn btn-dark"
                      onClick={() => setSelectedCar(car)}
                    >
                      Select
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredCars.length === 0 && (
          <p className="text-center text-muted mt-5">
            No cars found.
          </p>
        )}
      </main>

      <footer className="bg-dark text-white text-center py-4 mt-5">
        AutoPick © 2026
      </footer>
    </>
  );
}

export default App;
