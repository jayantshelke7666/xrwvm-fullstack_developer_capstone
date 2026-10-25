import React, { useState } from 'react';
import Header from '../Header/Header';
import './Register.css';

const Register = () => {
  const [values, setValues] = useState({ userName: '', firstName: '', lastName: '', email: '', password: '' });
  const [message, setMessage] = useState('');
  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value });
  const register = async (event) => {
    event.preventDefault();
    const response = await fetch('/djangoapp/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(values) });
    const result = await response.json();
    if (response.ok) { setMessage('Account created. You can now log in.'); window.location.href = '/login'; }
    else setMessage(result.status || 'Registration failed.');
  };
  return <div><Header/><main className="register_container"><h1 className="header">Sign-up</h1><form className="inputs" onSubmit={register}>
    <label className="input">Username <input required className="input_field" name="userName" value={values.userName} onChange={update}/></label>
    <label className="input">First Name <input required className="input_field" name="firstName" value={values.firstName} onChange={update}/></label>
    <label className="input">Last Name <input required className="input_field" name="lastName" value={values.lastName} onChange={update}/></label>
    <label className="input">Email <input required type="email" className="input_field" name="email" value={values.email} onChange={update}/></label>
    <label className="input">Password <input required type="password" className="input_field" name="password" value={values.password} onChange={update}/></label>
    <div className="submit_panel"><button className="submit" type="submit">Register</button><p role="status">{message}</p></div>
  </form></main></div>;
};
export default Register;
