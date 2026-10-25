import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

const Header = () => {
  const logout = async (event) => {
    event.preventDefault();
    await fetch('/djangoapp/logout', { method: 'GET' });
    ['username', 'firstname', 'lastname'].forEach(key => sessionStorage.removeItem(key));
    window.location.href = '/';
  };
  const username = sessionStorage.getItem('username');
  const accountLinks = username
    ? <div className="input_panel"><span className="username">{username}</span><a className="nav_item" href="/" onClick={logout}>Logout</a></div>
    : <div className="input_panel"><a className="nav_item" href="/login">Login</a><a className="nav_item" href="/register">Register</a></div>;
  return <nav className="navbar navbar-expand-lg navbar-light" style={{backgroundColor:'darkturquoise', minHeight:'1in'}}><div className="container-fluid"><a className="navbar-brand fw-bold" href="/">Dealerships</a><button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation"><span className="navbar-toggler-icon"/></button><div className="collapse navbar-collapse" id="navbarText"><ul className="navbar-nav me-auto mb-2 mb-lg-0"><li className="nav-item"><a className="nav-link" href="/dealers">Dealers</a></li><li className="nav-item"><a className="nav-link" href="/about">About Us</a></li><li className="nav-item"><a className="nav-link" href="/contact">Contact Us</a></li></ul><span className="navbar-text">{accountLinks}</span></div></div></nav>;
};
export default Header;
