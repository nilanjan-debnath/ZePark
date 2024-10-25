import React from 'react'
import { IoMenu } from "react-icons/io5";
import { FaSearchLocation } from "react-icons/fa";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";

export default function MapHeading() {

    const { currentUser } = useSelector((state) => state.user);

    return (
        <header className='w-full fixed top-0 left-0 z-10 flex justify-between items-center px-8 py-6'>
            <button className=""><IoMenu className='text-4xl' /></button>
            <div className="w-[22rem] h-12 border border-black  overflow-hidden flex rounded-full bg-[#D0B8A8]">
                <input type="text" className='w-[85%] h-full px-4 py-2 outline-none bg-transparent placeholder:text-black' placeholder='Search for Parking Spot...' />
                <button className="w-[15%] h-full flex justify-center items-center bg-transparent"><FaSearchLocation className='text-2xl' /></button>
            </div>
            <Link to='/profile'>
                <div className="w-12 h-12 rounded-full bg-blue-300 border border-black overflow-hidden">
                    <img src={currentUser.avatar} alt="" className='w-full h-full object-cover' />
                </div>
            </Link>
        </header>
    )
}
