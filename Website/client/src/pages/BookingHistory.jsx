import React from 'react'
import { FaArrowLeftLong, FaFileInvoiceDollar, FaLocationArrow } from "react-icons/fa6";
import { Link } from 'react-router-dom';

export default function BookingHistory() {
    return (
        <div className='w-full min-h-screen bg-[#F8EDE3]'>
            <div className="nav p-4 h-20 flex items-center sm:h-24 relative">
                <Link to='/profile'><FaArrowLeftLong className='text-3xl' />
                </Link>
                <h1 className='text-2xl font-semibold absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2'>Booking History</h1>
            </div>

            <div className="flex flex-col items-center gap-4 p-2">
                <div className="bg-[#D0B8A8] px-8 py-4 rounded-xl flex flex-col gap-2">
                    <h2 className='text-xl border-b-2 border-black pb-2 w-full'>Current Booking</h2>
                    <div className="flex items-center justify-between text-2xl font-semibold">
                        <h2>V-Mart Mall parking</h2>
                        <FaLocationArrow className='text-3xl text-[#C5705D]' />
                    </div>
                    <div className="text-xs sm:text-sm">
                        <p>Booking time: 10:39 am Friday, 11 October 2024 (IST)</p>
                        <p>Parking time: 10:45 am Friday, 11 October 2024 (IST)</p>
                    </div>
                    <div className="bg-[#C5705D] text-white p-2 text-2xl text-center rounded-xl font-semibold">
                        <h2>Slot No. A1 02</h2>
                        <h2>28 mins 30 secs</h2>
                    </div>
                    <p className='w-full text-center'>*slot charges: ₹50 per 30 mins</p>
                </div>
                <h1 className='text-2xl font-semibold w-[24rem] text-center pb-2 border-b-2 border-black my-4'>Privious Booking</h1>
                <div className="bg-[#DFD3C3] px-8 py-4 rounded-xl flex flex-col gap-2">
                    <div className="flex items-center justify-between text-2xl font-semibold">
                        <h2>Howrah A1 Praking</h2>
                        <FaLocationArrow className='text-3xl text-[#C5705D]' />
                    </div>
                    <div className="text-xs sm:text-sm">
                        <p>Booking time: 10:39 am Friday, 11 October 2024 (IST)</p>
                        <p>Parking time: 10:45 am Friday, 11 October 2024 (IST)</p>
                    </div>
                    <div className="px-8 sm:px-12">
                        <div className="w-full flex items-center border-2 border-[#C5705D] rounded-full overflow-hidden bg-white">
                            <div className="flex justify-center gap-4 items-center w-[60%] text-[#C5705D]">
                                <FaFileInvoiceDollar className='text-2xl' />
                                <h3 className='text-2xl font-semibold'>Bill</h3>
                            </div>
                            <h3 className="w-[40%] bg-[#C5705D] text-white px-4 py-2 text-center font-semibold rounded-full text-xl">&#x20b9; 160</h3>
                        </div>
                    </div>
                    <p className='w-full text-center'>*slot charges: ₹50 per 30 mins</p>
                </div>
            </div>
        </div>
    )
}
