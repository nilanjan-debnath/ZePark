import React, { useEffect, useState } from 'react';
import { MapContainer, CircleMarker, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';
import L from "leaflet";

import ChangeView from '../components/ChangeView';
import Routing from '../components/Routing';

import markerImage from "/images/marker logo.png";
import startImage from "/images/start logo.png";
import { RiPinDistanceFill } from "react-icons/ri";
import { CgMathEqual } from "react-icons/cg";
import MapHeading from '../components/MapHeading';
import InformationBox from '../components/InformationBox';

export default function Map() {

  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);
  const [destinationData, setDestinationData] = useState({
    lat: null,
    lon: null,
    name: null,
  });
  const [showMapbox, setShowMapbox] = useState(false);
  const [parkingLocations, setParkingLoactions] = useState(null);
  const [showInfoBox, setShowInfoBox] = useState(null);

  const maerkerIcon = new L.Icon({
    iconUrl: markerImage,
    iconSize: [35, 40],
    iconAnchor: [15, 35],
  });

  const startIcon = new L.Icon({
    iconUrl: startImage,
    iconSize: [40, 40],
  });

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.watchPosition((position) => {
        const { longitude, latitude } = position.coords;
        setLon(longitude);
        setLat(latitude);
      })
    }
  }, []);

  useEffect(() => {
    const fetchParkingSpot = async () => {
      try {
        const res = await fetch("/api/parking/allSpotData");
        const data = await res.json();
        if (data.success === false) {
          console.log(data.message);
          return;
        }
        setParkingLoactions(data);
      } catch (error) {
        console.log(error.message);
      }
    };
    fetchParkingSpot();
  }, []);

  if (!lat || !lon || !parkingLocations) {
    return <div className="w-full h-screen flex justify-center items-center bg-[#D0B8A8]">
      <div className="border-8 border-t-8 border-t-white border-gray-300 rounded-full w-16 h-16 animate-spin"></div>
    </div>
  }

  const setDestination = (name, lat, lon) => {
    console.log(name);
    setDestinationData({ lat, lon, name });
  }

  const distanceOfTwoSpot = (lat1, lon1, lat2, lon2) => {
    const lating1 = L.latLng(lat1, lon1);
    const lating2 = L.latLng(lat2, lon2);

    const distance = lating1.distanceTo(lating2);
    return (distance/1000).toFixed(1);
    // to convert the distance unit of KM
  }

  const sortedParkingSpot = () => {
    const sortedSpot = parkingLocations.map((spot) => ({
      ...spot,
      distance: distanceOfTwoSpot(22.5744, 88.3629, spot.latitude, spot.longitude)
    })).sort((a, b) => a.distance - b.distance);
    return sortedSpot;
  }

  const handleParkingBox = (spot) => {
    if(showInfoBox !== spot){
      setShowInfoBox(spot);
    }
  }

  return (
    <div className='w-full h-screen relative overflow-hidden'>
      <MapHeading />
      <MapContainer center={[22.5744, 88.3629]} zoom={14} scrollWheelZoom={true} zoomControl={false} className='z-0'>
        <TileLayer attribution='<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
          url="https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=xpL7wNLWmyhEZZoEtLXq" />

        {/* <ChangeView center={[lat, lon]} /> */}
        <ChangeView center={[22.5744, 88.3629]} />

        <CircleMarker center={[22.5744, 88.3629]} radius={12} color='white' fillColor='blue'>
          <Popup>
            <h1>My Location</h1>
          </Popup>
        </CircleMarker>

        {destinationData.lat && destinationData.lon && (
          <Marker position={[22.5744, 88.3629]} icon={startIcon}>
          </Marker>
        )}

        {parkingLocations.length !== 0 && (
          parkingLocations.map((data) =>
            <Marker key={data.name} position={[data.
              latitude, data.
              longitude]} eventHandlers={{ click: () => setDestination(data.name, data.latitude, data.longitude) }} icon={maerkerIcon}>
              <Popup>
                <h1>{data.name}</h1>
              </Popup>
            </Marker>
          )
        )}

        {destinationData.lat && destinationData.lon && (
          // <Routing lat={lat} lon={lon} destinationData={destinationData} />
          <Routing lat={22.5744} lon={88.3629} destinationData={destinationData} />
        )}
      </MapContainer>

        <InformationBox showInfoBox={showInfoBox} setShowInfoBox={setShowInfoBox} />
      <div className={`mapBox absolute border-2 border-[#C5705D] left-1/2 ${showMapbox ? 'bottom-0' : 'bottom-[-40%] 2xl:bottom-[-44%]'} -translate-x-1/2 z-10 px-4 pb-4 pt-0 bg-[#F8EDE3] transition-all duration-300 rounded-md`}>
        <button onClick={() => setShowMapbox(!showMapbox)} className="w-full mx-auto"><CgMathEqual className='text-4xl mx-auto' /></button>

        <div className="flex flex-col gap-4 h-[18rem] overflow-y-auto scrollbar-custom w-[22rem] px-2">
          {parkingLocations && sortedParkingSpot().map((spot, index) =>
            <div key={index} onClick={() => handleParkingBox(spot)} className="flex gap-6 border-2 border-[#C5705D] px-4 py-2 bg-[#D0B8A8] rounded-md cursor-pointer">
              <div className="left w-[80%] h-full">
                <h1 className='text-center mb-2 text-lg font-semibold truncate'>{spot.name}</h1>
                <div className="flex gap-4 justify-center items-center text-sm font-semibold">
                  <p>4.6 &#9733;</p>
                  <p className='px-2 py-1 bg-[#C5705D] text-white rounded-md'>Available</p>
                  <p>&#8377; {spot.pricing[spot.pricing.length > 1 ? 1 : 0].price} Rs/Hr</p>
                </div>
              </div>
              <div className="right w-[20%] h-full flex flex-col items-center">
                <RiPinDistanceFill className='w-6 h-6' />
                <h4 className='text-sm'>{spot.distance} Km</h4>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
