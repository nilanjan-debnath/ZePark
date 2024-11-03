import React, { useState } from 'react';
import { IoClose } from "react-icons/io5";
import { RiPinDistanceFill } from "react-icons/ri";

export default function InformationBox({ showInfoBox, setShowInfoBox }) {
    const [chosenPrice, setChosenPrice] = useState(0);
    
    const handleClose = () => {
        setShowInfoBox(null);
        setChosenPrice(0);
    }

    return (
        <div className="">
            {showInfoBox &&
                <div className='w-[23rem] absolute z-20 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 sm:w-[24rem]'>
                    <div className="w-full h-[8%] px-4">
                        <button onClick={handleClose} className="float-end"><IoClose className='w-10 h-10 text-[#C5705D]' /></button>
                    </div>
                    <div className="w-full p-4 pt-0 h-[92%]">
                        <div className=" w-full h-full border border-[#C5705D] bg-[#D0B8A8] rounded-3xl flex flex-col items-center p-2 gap-4 ">
                            <h1 className='text-2xl line-clamp-2 text-center font-semibold w-full px-4'>{showInfoBox.name}</h1>
                            <div className="flex px-3 gap-2 text-sm">
                                <p>{showInfoBox.address}</p>
                                <p className='text-xs'><RiPinDistanceFill className='text-2xl' />{showInfoBox.distance} Km</p>
                            </div>
                            <div className="flex items-center justify-between w-full px-4">
                                <p>Rating: <span className='py-1 px-2 rounded-md bg-[#C5705D] text-white text-sm font-semibold'>4.5 &#9733;</span></p>
                                <p>Avalaible Slots: <span className='py-1 px-2 rounded-md bg-[#C5705D] text-white text-sm font-semibold'>10/{showInfoBox.totalSlot}</span></p>
                            </div>
                            <div className="w-[80%] flex justify-between items-center text-xl border-b-2 border-black px-4 font-semibold">
                                <h2>Time Slots</h2>
                                <h2>Charges</h2>
                            </div>
                            <div className="w-[80%] h-40 py-2 flex flex-col gap-2 overflow-y-auto scrollbar-custom">
                                {showInfoBox.pricing.map((ele, index) =>
                                    <div key={index} onClick={()=> setChosenPrice(ele.price)} className={`flex justify-between items-center w-full py-2 px-6 rounded-md transition-all duration-300 hover:bg-white cursor-pointer border ${chosenPrice === ele.price? 'bg-white' : ''}`}>
                                        <div className="flex">
                                            <p className='w-8'>{ele.pro? 'Pro': ''}</p>
                                            <h3>{ele.time} Mins</h3>
                                        </div>
                                        <h3>&#8377; {ele.price}</h3>
                                    </div>
                                )}
                            </div>
                            <button className="bg-[#C5705D] text-white px-4 py-2 rounded-full w-[80%] font-semibold hover:bg-[#d45b3f] transition-all duration-300">Confirm Booking</button>
                            <p className='text-sm font-semibold'>*current Wallet Ballance <span className=''>&#8377; 1000</span></p>
                        </div>
                    </div>
                </div>
            }
        </div>
    )
}
