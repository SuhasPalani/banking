import React, { useState } from 'react';

export default function Banking() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    cardType: 'Credit Card',
    address: '',
    phone: '',
    dob: '',
    income: '',
    agreeTerms: false,
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
        setMessage('Application submitted successfully! We will get back to you soon.');
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
        <div className="form-group">
          <label>Address</label>
          <input
            type="text"
            placeholder="Enter your address"
            value={formData.address}
            onChange={(e) => setFormData({ ...formData, address: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label>Phone Number</label>
          <input
            type="tel"
            placeholder="Enter your phone number"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label>Date of Birth</label>
          <input
            type="date"
            value={formData.dob}
            onChange={(e) => setFormData({ ...formData, dob: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label>Income</label>
          <input
            type="number"
            placeholder="Enter your income"
            value={formData.income}
            onChange={(e) => setFormData({ ...formData, income: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={formData.agreeTerms}
              onChange={(e) => setFormData({ ...formData, agreeTerms: e.target.checked })}
              required
            />
            I agree to the <a href="/terms">terms and conditions</a>
          </label>
        </div>
        <button type="submit" disabled={!formData.agreeTerms}>
          Submit Application
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}
