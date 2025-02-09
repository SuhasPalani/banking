import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Admin() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if the provided credentials are for the superuser
    if (formData.email === "suhas@test" && formData.password === "suhas") {
      setMessage("Signin complete! Redirecting to Admin Console...");
      setTimeout(() => navigate("/admin_console"), 2000); // Redirect to Admin Console after 2 seconds
    } else {
      setMessage("Error: Invalid email or password");
    }
  };

  return (
    <div className="auth-form-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
          required
        />
        <button type="submit">Admin Sign In</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}
