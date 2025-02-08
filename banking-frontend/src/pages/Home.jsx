import React, { useState, useEffect } from 'react';
import BankCard from '../components/BankCard';

export default function Home() {
  const [banks, setBanks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBanks = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/banks');
        if (!response.ok) throw new Error('Failed to fetch banks');
        const data = await response.json();
        setBanks(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBanks();
  }, []);

  return (
    <main className="content">
      {loading ? (
        <div className="loading-spinner">Loading...</div>
      ) : error ? (
        <div className="error-message">⚠️ {error}</div>
      ) : (
        <div className="bank-grid">
          {banks.map(bank => (
            <BankCard key={bank.name} bank={bank} />
          ))}
        </div>
      )}
    </main>
  );
}
