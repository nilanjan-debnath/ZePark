import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function SignUp() {

  const [formData, setFormData] = useState({});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData, 
      [e.target.id]: e.target.value,
    });
  };

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try{
      const res = await fetch("/api/auth/signup", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if(data.success === false){
        setError(data.message);
        return;
      }
      navigate("/sign-in");
    }catch(error){
      setError(error.message);
    }finally {
      setLoading(false);
    }
  };

  return (
    <div className='flex justify-center items-center h-screen bg-[#C5FFF8]'>
      <div className="w-[28rem] p-4 rounded-3xl shadow-2xl bg-white">
        <h1 className='text-center text-3xl my-7'>Sign Up</h1>
        <form onSubmit={handleSubmit} className="flex flex-col justify-center my-4 p-4 gap-4">
          <input type="text" placeholder='Username' id='username' className='px-4 py-3 rounded-lg  border-2 border-gray-300' autoComplete='off' onChange={handleChange} required />
          <input type="email" placeholder='email' id='email' className='px-4 py-3 rounded-lg  border-2 border-gray-300' autoComplete='off' onChange={handleChange} required />
          <input type="password" placeholder='password' id='password' className='px-4 py-3 rounded-lg border-2 border-gray-300' autoComplete='off' onChange={handleChange} required />
          <input type="text" placeholder='contact' id='contact' className='px-4 py-3 rounded-lg border-2 border-gray-300' autoComplete='off' onChange={handleChange} required />
          <button className="bg-blue-600 text-xl text-white font-semibold w-full py-2 rounded-lg transition-all duration-300 hover:bg-blue-500 disabled:bg-blue-400">{loading?
            <div className="w-full h-full flex justify-center items-center">
              <div className="w-8 h-8 border-4 rounded-full border-t-4 border-t-gray-300 border-white animate-spin"></div> 
              </div>
            : 'Sign Up'}</button>
        </form>
        <p className='px-6 text-xs font-semibold my-4'>By continuing, you agree to Zeprak's Terms of Service and acknowledge you've read our Privacy Policy.Notice all collection</p>
        <div className="flex gap-2 px-4 my-8">
          <p>Already have an account ?</p>
          <Link to='/sign-in' className='text-blue-500 font-semibold'>Login</Link>
        </div>
      {error && (
        <p className="text-red-600 text-sm font-semibold px-4 text-center">{error}</p>
      )}
      </div>
    </div>
  )
}
