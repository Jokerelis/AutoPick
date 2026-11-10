
import { useState } from 'react';

const carImages = {
  'Volkswagen Golf': '/cars/golf.jpg',
  'Audi A6': '/cars/audi-a6.jpg',
  'Mazda MX-5': '/cars/mazda-mx5.jpg',
  'BMW X5': '/cars/bmw-x5.jpg',
  'Toyota Yaris': '/cars/yaris.jpg',
  'BMW 320': '/cars/bmw-320.jpg',
  'Subaru Forester': '/cars/forester.jpg',
  'BMW M4': '/cars/bmw-m4.jpg'
};
export default function CarCatalog({ cars, onSelect }) {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');

  const categories = [...new Set(cars.map(car => car.category))];

  const filteredCars = cars.filter(car =>
    (category === 'All' || car.category === category) &&
    `${car.brand} ${car.model}`.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <div className="row g-3 mb-4">
        <div className="col-md-8">
          <input className="form-control" placeholder="Search cars..."
                 value={search} onChange={e => setSearch(e.target.value)} />
        </div>

        <div className="col-md-4">
          <select className="form-select" value={category}
                  onChange={e => setCategory(e.target.value)}>
            <option value="All">All categories</option>
            {categories.map(c => <option key={c}>{c}</option>)}
          </select>
        </div>
      </div>

      <div className="row g-4">
        {filteredCars.map(car => (
          <div className="col-md-6 col-lg-4" key={car.id}>
            <div className="card car-card h-100">
              <div className="car-image">
                <img
                  src={
                    carImages[`${car.brand} ${car.model}`] ||
                    '/cars/default.jpg'
                  }
                  alt={`${car.brand} ${car.model}`}
                  loading="lazy"
                />
              </div>

              <div className="card-body">
                <span className="badge bg-secondary mb-2">{car.category}</span>
                <h5 className="fw-bold">{car.brand} {car.model}</h5>
                <p className="text-muted">{car.body_type}</p>

                <p>
                  Status: <span className={
                    car.status === 'Available' ? 'text-success' : 'text-danger'
                  }>{car.status}</span>
                </p>

                <div className="d-flex justify-content-between align-items-center">
                  <strong>€{car.base_price} / day</strong>

                  <button className="btn btn-dark"
                          disabled={car.status !== 'Available'}
                          onClick={() => onSelect(car)}>
                    Select
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredCars.length === 0 && (
        <p className="text-center text-muted mt-4">No cars found.</p>
      )}
    </>
  );
}
