import React, { useState, useEffect } from 'react';
import '../App.css';
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
    bankName: '',  // Add bankName to formData
  });
  const [banks, setBanks] = useState([]);
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch bank names from the backend when the component mounts
  useEffect(() => {
    const fetchBanks = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/banks');
        if (response.ok) {
          const data = await response.json();
          setBanks(data);
        } else {
          console.error("Error fetching banks:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching banks:", error);
      }
    };

    fetchBanks();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:5000/apply-card', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setMessage('Application submitted successfully! We will get back to you soon.');
        // Reset form after successful submission
        setFormData({
          name: '',
          email: '',
          cardType: 'Credit Card',
          address: '',
          phone: '',
          dob: '',
          income: '',
          agreeTerms: false,
          bankName: '',  // Reset bank name
        });
      } else {
        const errorData = await response.json();
        setMessage(`Error: ${errorData.message}`);
      }
    } catch (err) {
      setMessage(`Error: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="banking-page">
      <div className="form-container">
        <h2>Apply for a Card</h2>
        <form onSubmit={handleSubmit} className="card-application-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              type="text"
              placeholder="Enter your name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="cardType">Card Type</label>
            <select
              id="cardType"
              value={formData.cardType}
              onChange={(e) => setFormData({ ...formData, cardType: e.target.value })}
            >
              <option value="Credit Card">Credit Card</option>
              <option value="Debit Card">Debit Card</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="bankName">Select Bank</label>
            <select
              id="bankName"
              value={formData.bankName}
              onChange={(e) => setFormData({ ...formData, bankName: e.target.value })}
              required
            >
              <option value="">Select a bank</option>
              {banks.map((bank) => (
                <option key={bank.name} value={bank.name}>
                  {bank.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="address">Address</label>
            <input
              id="address"
              type="text"
              placeholder="Enter your address"
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone">Phone Number</label>
            <input
              id="phone"
              type="tel"
              placeholder="Enter your phone number"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              required
              pattern="[0-9]{10}"
              title="Please enter a valid 10-digit phone number"
            />
          </div>

          <div className="form-group">
            <label htmlFor="dob">Date of Birth</label>
            <input
              id="dob"
              type="date"
              value={formData.dob}
              onChange={(e) => setFormData({ ...formData, dob: e.target.value })}
              required
              max={new Date().toISOString().split('T')[0]}
            />
          </div>

          <div className="form-group">
            <label htmlFor="income">Annual Income</label>
            <input
              id="income"
              type="number"
              placeholder="Enter your annual income"
              value={formData.income}
              onChange={(e) => setFormData({ ...formData, income: e.target.value })}
              required
              min="0"
              step="1000"
            />
          </div>

          <div className="form-group checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={formData.agreeTerms}
                onChange={(e) => setFormData({ ...formData, agreeTerms: e.target.checked })}
                required
              />
              <span>I agree to the <a href="/terms" target="_blank" rel="noopener noreferrer">terms and conditions</a></span>
            </label>
          </div>

          <button 
            type="submit" 
            disabled={!formData.agreeTerms || isSubmitting}
            className={isSubmitting ? 'submitting' : ''}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Application'}
          </button>
        </form>

        {message && (
          <p className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}
