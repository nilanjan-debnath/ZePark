import React, { useState } from 'react';
import {Link, useNavigate} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import { signInFailure, signInStart, signInSuccess } from '../redux/user/userSlice';

export default function SignIn() {

  const [formData, setFormData] = useState({});
  const navigate = useNavigate();

  const dispatch = useDispatch();
  const {loading, error} = useSelector((state) => state.user);

  const handleChange = (e) => {
    setFormData({...formData, [e.target.id]: e.target.value});
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    try{
      dispatch(signInStart());
      const res = await fetch("/api/auth/signin", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if(data.success === false){
        dispatch(signInFailure(data.message));
        return;
      }
      dispatch(signInSuccess(data));
      navigate("/home-map");
    }catch(error){
      dispatch(signInFailure(error.message));
    }
  }

  return (
    <div className='flex justify-center items-center h-screen bg-[#F8EDE3]'>
      <div className="w-[28rem] p-4 rounded-3xl shadow-2xl bg-white">
        <h1 className='text-center text-3xl my-7'>Login</h1>
        <form onSubmit={handleSubmit} className="flex flex-col justify-center my-4 p-4 gap-4">
          <input type="email" placeholder='email' id='email' className='px-4 py-3 rounded-lg  border-2 border-gray-300' autoComplete='off' onChange={handleChange} required />
          <input type="password" placeholder='password' id='password' className='px-4 py-3 rounded-lg border-2 border-gray-300' autoComplete='off' onChange={handleChange} required />
          <button className="bg-[#C5705D] text-xl text-white font-semibold w-full py-2 rounded-lg transition-all duration-300 hover:bg-[#CA634C] disabled:bg-[#E48F7C]">{loading?
            <div className="w-full h-full flex justify-center items-center">
              <div className="w-8 h-8 border-4 rounded-full border-t-4 border-t-gray-300 border-white animate-spin"></div> 
              </div>
            : 'Login'}</button>
        </form>
        <p className='px-6 text-xs font-semibold my-4'>By continuing, you agree to Zeprak's Terms of Service and acknowledge you've read our Privacy Policy.Notice all collection</p>
        <p className='px-4 text-sm'>Forget Password? <Link to="" className='text-blue-500 font-semibold'>Click Here</Link></p>
        <div className="flex gap-2 px-4 my-2">
          <p>Don't have an account?</p>
          <Link to='/sign-up' className='text-blue-500 font-semibold'>Sign Up</Link>
        </div>
      {error && (
        <p className="text-red-600 text-sm font-semibold px-4 text-center">{error}</p>
      )}
      </div>
    </div>
  )
}
