import React from 'react'
import { FaArrowLeftLong } from "react-icons/fa6";
import { useSelector } from 'react-redux';
import { FaPencilAlt, FaHistory, FaUserShield, FaQuestionCircle,FaPowerOff } from "react-icons/fa";
import { IoWalletSharp, IoCarSport } from "react-icons/io5";
import { IoIosArrowForward } from "react-icons/io";
import { Link } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { signOutFailure, signOutStart, signOutSuccess } from '../redux/user/userSlice';
import { useNavigate } from 'react-router-dom';

export default function Profile() {

    const { currentUser } = useSelector((state) => state.user);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try{
            dispatch(signOutStart());
            const res = await fetch("/api/auth/logout");
            const data = await res.json();
            if(data.success === false){
                dispatch(signOutFailure(data.message));
                return;
            }
            dispatch(signOutSuccess());
            navigate("/sign-in");
        }catch(error){
            dispatch(signOutFailure(error.message));
        }
    };

    return (
        <>
            {currentUser &&
                <div className='w-full bg-[#F8EDE3]'>
                    <div className="nav px-4 h-12 flex items-center sm:h-16">
                        <Link to='/home-map'><FaArrowLeftLong className='text-3xl' />
                        </Link>
                    </div>
                    <div className="h-[90%] w-full flex items-center flex-col gap-2 py-4">
                        <div className="relative">
                            <div className="w-24 h-24 rounded-full bg-blue-300 overflow-hidden border-2 border-[#C5705D] sm:w-28 sm:h-28">
                                <img src={currentUser.avatar} alt="" className="w-full h-full object-cover" />
                            </div>
                            <button className="absolute bottom-[10%] left-[75%] text-white bg-[#C5705D] p-2 rounded-full"><FaPencilAlt className='text-lg' /></button>
                        </div>
                        <h3 className='text-lg font-semibold'>{currentUser.username}</h3>
                        <h3 className='text-xl font-semibold text-[#A17B7B]'>WB 17 MF 1530</h3>
                        <button className="px-8 py-2 rounded-full text-white bg-[#C5705D] font-semibold">Update to Pro</button>
                        <div className="btmBox flex flex-col justify-center items-center gap-4 w-[22rem] p-4 sm:w-[26rem]">
                            <div className="flex justify-between border-2 border-[#C5705D] w-full px-4 py-3 text-lg font-semibold rounded-full relative mb-4 bg-white">
                                <div className="flex gap-4 text-[#C5705D]"><IoWalletSharp className='text-3xl'/> Wallet</div>
                                <div className="px-4 bg-[#C5705D] text-white absolute right-0 top-0 h-full rounded-full flex justify-center items-center w-[40%] text-xl">&#x20b9; {currentUser.wallet}</div>
                            </div>
                            <div className="w-full pl-8 pr-4 py-3 flex items-center justify-between rounded-full bg-[#DFD3C3]">
                                <div className="flex gap-8 items-center text-lg">
                                <FaHistory className='text-2xl'/>
                                Booking History
                                </div>
                                <IoIosArrowForward className='text-3xl'/>
                            </div>
                            <div className="w-full pl-8 pr-4 py-3 flex items-center justify-between rounded-full bg-[#DFD3C3]">
                                <div className="flex gap-8 items-center text-lg">
                                <IoCarSport className='text-2xl'/>
                                Car Details
                                </div>
                                <IoIosArrowForward className='text-3xl'/>
                            </div>
                            <div className="w-full pl-8 pr-4 py-3 flex items-center justify-between rounded-full bg-[#DFD3C3]">
                                <div className="flex gap-8 items-center text-lg">
                                <FaUserShield className='text-2xl'/>
                                Privacy
                                </div>
                                <IoIosArrowForward className='text-3xl'/>
                            </div>
                            <div className="w-full pl-8 pr-4 py-3 flex items-center justify-between rounded-full bg-[#DFD3C3]">
                                <div className="flex gap-8 items-center text-lg">
                                <FaQuestionCircle className='text-2xl'/>
                                Help & Support
                                </div>
                                <IoIosArrowForward className='text-3xl'/>
                            </div>
                            <button onClick={handleLogout} className="w-full pl-8 pr-4 py-3 flex items-center justify-between rounded-full bg-[#DFD3C3]">
                                <div className="flex gap-8 items-center text-lg">
                                <FaPowerOff className='text-2xl'/>
                                Logout
                                </div>
                                <IoIosArrowForward className='text-3xl'/>
                            </button>
                        </div>
                    </div>
                </div>
            }
        </>
    )
}
