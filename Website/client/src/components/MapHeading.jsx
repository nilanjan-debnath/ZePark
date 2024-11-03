import React from 'react'
import { IoMenu } from "react-icons/io5";
import { FaSearchLocation } from "react-icons/fa";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";

export default function MapHeading() {

    const { currentUser } = useSelector((state) => state.user);

    return (
        <header className='w-full fixed top-0 left-0 z-10 flex justify-between items-center px-2 py-6 sm:px-8'>
            <button className=""><IoMenu className='text-3xl sm:text-4xl' /></button>
            <div className="w-[13rem] h-12 border border-black  overflow-hidden flex rounded-full bg-[#D0B8A8] sm:w-[22rem]">
                <input type="text" className='w-[80%] h-full px-4 py-1 outline-none bg-transparent placeholder:text-black sm:w-[85%] sm:py-2' placeholder='Search for Parking Spot...' />
                <button className="w-[20%] h-full flex justify-center items-center bg-transparent sm:w-[15%]"><FaSearchLocation className='text-xl sm:text-2xl' /></button>
            </div>
            <Link to='/profile'>
                <div className="w-10 h-10 rounded-full bg-blue-300 border border-black overflow-hidden sm:w-12 sm:h-12">
                    <img src={currentUser.avatar} alt="" className='w-full h-full object-cover' />
                </div>
            </Link>
        </header>
    )
}
