import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom';

export default function AddSpot() {

    const {currentUser} = useSelector((state) => state.user);
    const [formData, setFormData] = useState({
        ownerName: currentUser.username,
        name: "",
        contact: currentUser.contact,
        latitude: "",
        longitude: "",
        address: "",
        totalSlot: "",
        userRef: currentUser._id,
    })
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({
            ...formData, [e.target.id]: e.target.value,
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try{
            const res = await fetch(`/api/parking/addSpot/${currentUser._id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const data = await res.json();
            if(data.success === false){
                console.log(data.message);
                setLoading(false);
                setError(data.message);
                return;
            }
            navigate(`/add-pricing/${data._id}`);
        }catch(error){
            console.log(error.message);
            setError(error.message);
        }finally{
            setLoading(false);
        }
    }

  return (
    <div className='bg-[#F8EDE3] w-full h-screen flex justify-center items-center flex-col'>
        <h1 className="text-3xl">Add Parking Spot</h1>
      <div className="form  p-8 w-[30rem] rounded-xl ">
        <form onSubmit={handleSubmit} className="flex justify-center items-center flex-col gap-4 w-full h-full">
            <input type="text" className="px-4 py-3 w-full rounded-md border border-black outline-none" placeholder='Ownername' id='ownerName' required autoComplete='off' defaultValue={formData.ownerName} onChange={handleChange}/>
            <input type="text" className="px-4 py-3 w-full rounded-md border border-black outline-none" placeholder='Name' id='name' required autoComplete='off' defaultValue={formData.name} onChange={handleChange}/>
            <input type="text" className="px-4 py-3 w-full rounded-md border border-black outline-none" placeholder='Contact' id='contact' required autoComplete='off' defaultValue={formData.contact} onChange={handleChange}/>
            <input type="number" className="px-4 py-3 w-full rounded-md border border-black outline-none" placeholder='Latitude' id='latitude' required autoComplete='off' defaultValue={formData.latitude} onChange={handleChange}/>
            <input type="number" className="px-4 py-3 w-full rounded-md border border-black outline-none" placeholder='Longitude' id='longitude' required autoComplete='off' defaultValue={formData.longitude} onChange={handleChange}/>
            <input type="text" className="px-4 py-3 w-full rounded-md border border-black outline-none" placeholder='Address' id='address' required autoComplete='off' defaultValue={formData.address} onChange={handleChange}/>
            <input type="number" className="px-4 py-3 w-full rounded-md border border-black outline-none" placeholder='Total Slot' id='totalSlot' required autoComplete='off' defaultValue={formData.totalSlot} onChange={handleChange}/>
            <button disabled={loading} className='px-4 py-3 rounded-md text-white bg-[#C5705D] w-full font-semibold text-lg disabled:bg-[#BF8D81]'>{loading? 
            <div className="w-full h-full flex justify-center items-center">
            <div className="w-8 h-8 border-4 rounded-full border-t-4 border-t-gray-300 border-white animate-spin"></div> 
            </div>
            : 'Submit'}</button>
        </form>
        {error && <p className='font-semibold text-red-600 text-center'>{error}</p>}
      </div>
    </div>
  )
}
