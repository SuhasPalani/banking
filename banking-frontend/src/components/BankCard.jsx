import React, { useState } from 'react';

export default function BankCard({ bank }) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div 
      className={`bank-card ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <h3>{bank.name}</h3>

      {isHovered && (
        <div className="bank-details">
          <p><strong>Type:</strong> {bank.type}</p>
          <p><strong>Contact:</strong> {bank.contact_details.phone}</p>
          <a href={bank.contact_details.website} target="_blank" rel="noopener noreferrer">
            Visit Website
          </a>

          <h4>Services:</h4>
          <ul>
            {bank.services.map(service => (
              <li key={service}>{service}</li>
            ))}
          </ul>

          <h4>Online Features:</h4>
          <ul>
            {bank.online_features.map(feature => (
              <li key={feature}>{feature}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
