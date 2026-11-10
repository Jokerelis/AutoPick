
import { useState } from 'react';

export default function CompanyLogin({ onConnect }) {
  const [companyId, setCompanyId] = useState('1');
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await onConnect(companyId, apiKey.trim());
      setApiKey('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card shadow-sm mx-auto" style={{ maxWidth: 500 }}>
      <div className="card-body p-4">
        <h3 className="mb-3">Select rental company</h3>

        <form onSubmit={handleSubmit}>
          <label className="form-label">Company</label>
          <select className="form-select mb-3" value={companyId}
                  onChange={e => setCompanyId(e.target.value)}>
            <option value="1">AutoPick Vilnius</option>
            <option value="2">AutoPick Kaunas</option>
          </select>

          <label className="form-label">API Key</label>
          <input type="password" className="form-control mb-3"
                 required autoComplete="off"
                 value={apiKey}
                 onChange={e => setApiKey(e.target.value)} />

          {error && <div className="alert alert-danger">{error}</div>}

          <button className="btn btn-dark w-100" disabled={loading}>
            {loading ? 'Connecting...' : 'Continue'}
          </button>
        </form>
      </div>
    </div>
  );
}
