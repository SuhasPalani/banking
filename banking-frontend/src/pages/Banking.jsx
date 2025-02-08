import React, { useState } from 'react';

export default function Banking() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    cardType: 'Credit Card',
  });
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/apply-card', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setMessage('Application submitted successfully!');
      } else {
        const errorData = await response.json();
        setMessage(`Error: ${errorData.message}`);
      }
    } catch (err) {
      setMessage(`Error: ${err.message}`);
    }
  };

  return (
    <div className="banking-page">
      <h2>Apply for a Card</h2>
      <form onSubmit={handleSubmit} className="card-application-form">
        <div className="form-group">
          <label>Name</label>
          <input
            type="text"
            placeholder="Enter your name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label>Card Type</label>
          <select
            value={formData.cardType}
            onChange={(e) => setFormData({ ...formData, cardType: e.target.value })}
          >
            <option value="Credit Card">Credit Card</option>
            <option value="Debit Card">Debit Card</option>
          </select>
        </div>
        <button type="submit">Submit Application</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}
