import React, { useEffect, useState } from 'react';
import { MdDelete } from "react-icons/md";
import { useParams, useNavigate } from "react-router-dom";

export default function AddPricing() {

    const [pricingData, setPricingData] = useState([{
        time: '',
        price: '',
        pro: false,
    }]);
    const params = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [spotData, setSpotData] = useState(null);
    console.log(pricingData);

    const handleChange = (e, index) => {
        const newData = [...pricingData];
        if (e.target.type === 'checkbox') {
            newData[index][e.target.id] = e.target.checked ? true : false;
        } else {
            newData[index][e.target.id] = e.target.value;
        }
        setPricingData(newData);
    };

    const addRow = () => {
        setPricingData([...pricingData, { time: '', price: '', pro: false, }]);
    };

    const removeRow = (idx) => {
        if (idx > 0) {
            const newData = pricingData.filter((_, index) => idx !== index);
            setPricingData(newData);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`/api/parking/addPricing/${params.spotId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(pricingData),
            });
            const data = await res.json();
            if (data.success === false) {
                setError(data.message);
                return;
            }
            navigate("/home-map");
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const fetchSpotData = async () => {
            try {
                const res = await fetch(`/api/parking/spotDetails/${params.spotId}`);
                const data = await res.json();
                if (data.success === false) {
                    console.log(data.message);
                    return;
                }
                setSpotData(data);
                // if(data.pricing && data.pricing.length > 0){
                //     setPricingData(data.pricing.map(({ _id, ...rest }) => rest));
                //     // this line help to remove all the id's from the array.
                // }
            } catch (error) {
                console.log(error.message);
            }
        };

        fetchSpotData();
    }, []);

    return (
        <div>
            {!spotData && <div className="w-full h-screen flex justify-center items-center bg-[#D0B8A8]">
                <div className="border-8 border-t-8 border-t-white border-gray-300 rounded-full w-20 h-20 animate-spin"></div>
            </div>}

            {spotData && (
                <div className='bg-[#F8EDE3] w-full h-screen flex items-center flex-col py-10 gap-4'>
                    <div className="flex flex-col gap-4 w-[56rem] px-2 mb-8">
                        <h1 className='text-xl'><span className='font-semibold mr-2'>Parking Name: </span>{spotData.name}</h1>
                        <h1 className='text-xl'><span className='font-semibold mr-2'>Owner Name: </span>{spotData.ownerName}</h1>
                        <h1 className='text-xl'><span className='font-semibold mr-2'>Total Slot:</span>{spotData.totalSlot}</h1>
                    </div>
                    <div className="border-2 border-black p-4 w-[56rem] rounded-md">
                        <h1 className='text-2xl font-semibold'>Add Pricing</h1>
                        <p className='py-2'>Add the minimum time and price for the parking slots. Be careful, as this pricing will be displayed for this location. For more information <span className='text-blue-700 font-semibold cursor-pointer'>Click Here</span></p>
                        <form onSubmit={handleSubmit} className="py-2">
                            {pricingData.map((entry, index) => (
                                <div key={index} className="border p-3 flex justify-between">
                                    <div className="flex gap-4 w-[90%]">
                                        <input type="number" className="px-4 py-2 border border-black w-[35%] rounded-md" id='time' placeholder='Time (Min)' required autoComplete='off' onChange={(e) => handleChange(e, index)} defaultValue={entry.time} />
                                        <input type="number" className="px-4 py-2 border border-black w-[35%] rounded-md" id='price' placeholder='Price (Rs)' required autoComplete='off' onChange={(e) => handleChange(e, index)} defaultValue={entry.price} />
                                        <div className="flex items-center gap-2 ml-2">
                                            <label htmlFor="pro">Pro Users: </label>
                                            <input type="checkbox" className='w-[1.2rem] h-[1.2rem]' id='pro' onChange={(e) => handleChange(e, index)} defaultValue={entry.pro} />
                                        </div>
                                    </div>
                                    {index > 0 &&
                                        <button type='button' onClick={() => removeRow(index)} className="bg-red-500 text-white px-3 rounded-full transition-all duration-300 hover:bg-red-600"><MdDelete className='text-xl' /></button>
                                    }
                                </div>
                            ))}
                            <div className="w-full flex justify-end p-2">
                                <button onClick={addRow} type='button' className="px-3 py-1 bg-[#B48260] text-white rounded-sm">Add More</button>
                            </div>
                            <button className="px-4 py-3 bg-[#C5705D] text-white rounded-md w-[10rem] font-semibold">{loading ?
                                <div className="w-full h-full flex justify-center items-center">
                                    <div className="w-8 h-8 border-4 rounded-full border-t-4 border-t-gray-300 border-white animate-spin"></div>
                                </div>
                                : 'Submit'}</button>
                        </form>
                        {error && <p className='text-red-600 font-semibold text-center'>{error}</p>}
                    </div>
                </div>

            )}
        </div>
    )
}
