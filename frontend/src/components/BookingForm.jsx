
import { useState } from 'react';

const fields = [
  { name: 'start_date', label: 'Start date', type: 'date' },
  { name: 'end_date', label: 'End date', type: 'date' },
  { name: 'driver_age', label: 'Driver age', type: 'number', min: 20, step: 1 },
  { name: 'driving_experience', label: 'Driving experience (years)', type: 'number', min: 1, step: 0.5 }
];

const bodyTypes = [
  'SUV', 'Sedan', 'Hatchback', 'Convertible', 'Coupe'
];

export default function BookingForm({ car, cars, session, onClose }) {
  const [activeCar, setActiveCar] = useState(car);
  const [form, setForm] = useState({
    start_date: '',
    end_date: '',
    driver_age: '',
    driving_experience: '',
    preferred_body_type: ''
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [alternatives, setAlternatives] = useState([]);
  const [recommendationSource, setRecommendationSource] = useState('');
  const [loading, setLoading] = useState(false);

  async function reserve(e) {
    e.preventDefault();

    if (loading) return;

    setLoading(true);
    setError('');
    setAlternatives([]);
    setRecommendationSource('');
    setResult(null);

    try {
      const response = await fetch(
        `/api/companies/${session.companyId}/reservations`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': session.apiKey
          },
          body: JSON.stringify({
            ...form,
            car_id: activeCar.id,
            driver_age: Number(form.driver_age),
            driving_experience: Number(form.driving_experience)
          })
        }
      );

      const data = await response.json();

      if (response.status === 409) {
        setError(data.detail?.message || 'Car is unavailable');
        setAlternatives(data.detail?.alternatives || []);
        setRecommendationSource(
          data.detail?.recommendation_source || 'Fallback'
        );
      } else if (!response.ok) {
        const detail = data.detail;

        throw new Error(
          typeof detail === 'string'
            ? detail
            : Array.isArray(detail)
              ? detail.map(x => x.msg).join(', ')
              : detail?.message || 'Reservation failed'
        );
      } else {
        setResult(data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function chooseAlternative(id) {
    const alternative = cars.find(c => c.id === id);

    if (!alternative) return;

    setActiveCar(alternative);
    setError('');
    setResult(null);
    setAlternatives([]);
    setRecommendationSource('');
  }

  return (
    <div className="card shadow-sm mb-5">
      <div className="card-body p-4">
        <div className="d-flex justify-content-between align-items-center">
          <h4>
            Reserve {activeCar.brand} {activeCar.model}
          </h4>

          <button
            type="button"
            className="btn-close"
            onClick={onClose}
            aria-label="Close"
          />
        </div>

        <p className="text-muted">
          Base price: €{activeCar.base_price} / day
        </p>

        <form onSubmit={reserve}>
          <div className="row g-3">
            {fields.map(field => (
              <div className="col-md-6" key={field.name}>
                <label className="form-label">
                  {field.label}
                </label>

                <input
                  className="form-control"
                  type={field.type}
                  min={
                    field.name === 'end_date'
                      ? form.start_date || undefined
                      : field.min
                  }
                  step={field.step}
                  required
                  value={form[field.name]}
                  onChange={e => setForm({
                    ...form,
                    [field.name]: e.target.value
                  })}
                />
              </div>
            ))}
          </div>

          <div className="mt-3">
            <label className="form-label">
              Preferred body type (optional)
            </label>

            <select
              className="form-select"
              value={form.preferred_body_type}
              onChange={e => setForm({
                ...form,
                preferred_body_type: e.target.value
              })}
            >
              <option value="">No preference</option>

              {bodyTypes.map(type => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="btn btn-dark mt-4"
            disabled={loading || result !== null}
          >
            {loading ? 'Processing...' : 'Reserve car'}
          </button>
        </form>

        {result && (
          <div className="alert alert-success mt-4">
            <strong>Reservation confirmed!</strong>

            <div>Reservation ID: {result.id}</div>
            <div>Status: {result.status}</div>
            <div>
              Total price: €{Number(result.total_price).toFixed(2)}
            </div>
          </div>
        )}

        {error && (
          <div className="alert alert-danger mt-4">
            {error}
          </div>
        )}

        {alternatives.length > 0 && (
          <div className="mt-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">Available alternatives</h5>

              <span className={`badge ${
                recommendationSource === 'AI'
                  ? 'bg-success'
                  : 'bg-secondary'
              }`}>
                {recommendationSource === 'AI'
                  ? 'AI Recommendation'
                  : 'Fallback Recommendation'}
              </span>
            </div>

            {alternatives.map((alt, index) => (
              <div
                className="border rounded p-3 mb-2 d-flex justify-content-between align-items-center"
                key={alt.car_id}
              >
                <div>
                  <strong>
                    {alt.brand} {alt.model}
                  </strong>

                  {index === 0 && recommendationSource === 'AI' && (
                    <span className="badge bg-success ms-2">
                      AI Pick
                    </span>
                  )}

                  <div className="text-muted">
                    {alt.category} · {alt.body_type}
                  </div>

                  <div className="fw-bold">
                    €{Number(alt.total_price).toFixed(2)}
                  </div>
                </div>

                <button
                  type="button"
                  className="btn btn-outline-dark"
                  onClick={() => chooseAlternative(alt.car_id)}
                >
                  Select
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
