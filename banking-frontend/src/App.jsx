import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Banking from './pages/Banking';
import Admin from './pages/Admin';
import AdminConsole from './pages/AdminConsole';
import './App.css';

export default function App() {
  return (
    <Router>
      <Main />
    </Router>
  );
}

function Main() {
  const location = useLocation();

  return (
    <div className="app">
      {/* Render navbar only if not on the Banking page */}
      {location.pathname !== '/banking' && location.pathname !== '/admin' && location.pathname !== '/admin_console' &&(
        <nav className="main-nav">
          <div className="nav-brand">
            <Link to="/" className="nav-link">Banking Portal</Link>
          </div>
          <div className="nav-links">
            <Link to="/signin" className="nav-btn">Sign In</Link>
            <Link to="/signup" className="nav-btn primary">Sign Up</Link>
            <Link to="/admin" className="nav-btn primary">Admin</Link>
          </div>
        </nav>
      )}

      {/* Define routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/banking" element={<Banking />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/admin_console" element={<AdminConsole />} />
      </Routes>
    </div>
  );
}
