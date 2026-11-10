
import { useState } from 'react';
import './App.css';

function App() {
  const [companyId, setCompanyId] = useState('1');
  const [apiKey, setApiKey] = useState('');
  const [session, setSession] = useState(null);

  const [cars, setCars] = useState([]);
  const [category, setCategory] = useState('All');
  const [search, setSearch] = useState('');
  const [selectedCar, setSelectedCar] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function connectCompany(event) {
    event.preventDefault();

    if (!apiKey.trim()) {
      setError('Please enter an API key.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(
        `/api/companies/${companyId}/cars`,
        {
          headers: {
            'X-API-Key': apiKey.trim()
          }
        }
      );

      if (response.status === 401 || response.status === 403) {
        throw new Error('Invalid API key for this company.');
      }

      if (!response.ok) {
        throw new Error('Failed to load cars.');
      }

      const data = await response.json();

      setCars(data);
      setSession({
        companyId: companyId,
        apiKey: apiKey.trim()
      });
      setApiKey('');

    } catch (err) {
      setError(err.message);
      setCars([]);
    } finally {
      setLoading(false);
    }
  }

  function disconnectCompany() {
    setSession(null);
    setApiKey('');
    setCars([]);
    setSelectedCar(null);
    setSearch('');
    setCategory('All');
    setError('');
  }

  const filteredCars = cars.filter((car) => {
    const matchesCategory =
      category === 'All' || car.category === category;

    const carName =
      `${car.brand} ${car.model}`.toLowerCase();

    const matchesSearch =
      carName.includes(search.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  const companyName =
    session?.companyId === '1'
      ? 'AutoPick Vilnius'
      : 'AutoPick Kaunas';

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

        {!session ? (
          <div className="card shadow-sm mx-auto"
               style={{ maxWidth: '500px' }}>
            <div className="card-body p-4">

              <h3 className="fw-bold mb-3">
                Select rental company
              </h3>

              <form onSubmit={connectCompany}>

                <label className="form-label">
                  Company
                </label>

                <select
                  className="form-select mb-3"
                  value={companyId}
                  onChange={(e) => {
                    setCompanyId(e.target.value);
                    setError('');
                  }}
                >
                  <option value="1">AutoPick Vilnius</option>
                  <option value="2">AutoPick Kaunas</option>
                </select>

                <label className="form-label">
                  API Key
                </label>

                <input
                  type="password"
                  className="form-control mb-3"
                  placeholder="Enter your API key"
                  autoComplete="off"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                />

                {error && (
                  <div className="alert alert-danger">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  className="btn btn-dark w-100"
                  disabled={loading}
                >
                  {loading ? 'Connecting...' : 'Continue'}
                </button>
              </form>
            </div>
          </div>

        ) : (
          <>
            <div className="d-flex justify-content-between
                            align-items-center mb-4">

              <div>
                <h2 className="fw-bold mb-1">
                  Available cars
                </h2>
                <p className="text-muted mb-0">
                  {companyName}
                </p>
              </div>

              <button
                className="btn btn-outline-dark"
                onClick={disconnectCompany}
              >
                Switch company
              </button>
            </div>

            <div className="row g-3 mb-4">
              <div className="col-md-8">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Search cars..."
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
                Selected: {selectedCar.brand} {selectedCar.model}
              </div>
            )}

            <div className="row g-4">
              {filteredCars.map((car) => (
                <div
                  className="col-md-6 col-lg-4"
                  key={car.id}
                >
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

                      <p>
                        Status:{' '}
                        <span className={
                          car.status === 'Available'
                            ? 'text-success'
                            : 'text-danger'
                        }>
                          {car.status}
                        </span>
                      </p>

                      <div className="d-flex justify-content-between
                                      align-items-center">
                        <div>
                          <span className="fs-4 fw-bold">
                            €{car.base_price}
                          </span>
                          <span className="text-muted">
                            {' '}/ day
                          </span>
                        </div>

                        <button
                          className="btn btn-dark"
                          disabled={car.status !== 'Available'}
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
          </>
        )}
      </main>

      <footer className="bg-dark text-white text-center py-4 mt-5">
        AutoPick © 2026
      </footer>
    </>
  );
}

export default App;
