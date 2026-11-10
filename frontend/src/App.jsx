
import { useState } from 'react';
import CompanyLogin from './components/CompanyLogin';
import CarCatalog from './components/CarCatalog';
import BookingForm from './components/BookingForm';
import './App.css';

function App() {
  const [session, setSession] = useState(null);
  const [cars, setCars] = useState([]);
  const [selectedCar, setSelectedCar] = useState(null);

  async function connectCompany(companyId, apiKey) {
    const response = await fetch(`/api/companies/${companyId}/cars`, {
      headers: { 'X-API-Key': apiKey }
    });

    if (!response.ok) {
      throw new Error(
        response.status === 401 || response.status === 403
          ? 'Invalid API key for this company'
          : 'Failed to load cars'
      );
    }

    setCars(await response.json());
    setSession({ companyId, apiKey });
    setSelectedCar(null);
  }

  function disconnectCompany() {
    setSession(null);
    setCars([]);
    setSelectedCar(null);
  }

  return (
    <>
      <nav className="navbar navbar-dark bg-dark">
        <div className="container">
          <span className="navbar-brand fw-bold">AutoPick</span>
          <span className="text-white-50">Car Rental</span>
        </div>
      </nav>

      <header className="hero">
        <div className="container">
          <h1 className="display-5 fw-bold">Find your perfect car</h1>
          <p className="lead">Choose a car and enjoy a simple rental experience.</p>
        </div>
      </header>

      <main className="container py-5">
        {!session ? (
          <CompanyLogin onConnect={connectCompany} />
        ) : (
          <>
            <div className="d-flex justify-content-between mb-4">
              <h2>Available cars</h2>
              <button className="btn btn-outline-dark"
                      onClick={disconnectCompany}>
                Switch company
              </button>
            </div>

            {selectedCar && (
              <BookingForm
                key={selectedCar.id}
                car={selectedCar}
                cars={cars}
                session={session}
                onClose={() => setSelectedCar(null)}
              />
            )}

            <CarCatalog cars={cars} onSelect={setSelectedCar} />
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
