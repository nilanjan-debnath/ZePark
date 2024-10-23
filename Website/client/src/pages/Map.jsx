import React, { useEffect, useState } from 'react';
import { MapContainer, CircleMarker, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';

import ChangeView from '../components/ChangeView';
import Routing from '../components/Routing';

export default function Map() {

  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);
  const [destinationData, setDestinationData] = useState({
    lat: null,
    lon: null,
    name: null,
  });
  console.log("destination: ", destinationData);

  let parkingLocations = [
    { name: "Howrah", lat: 22.5839, lon: 88.3434 },
    { name: "Sealdah", lat: 22.5678, lon: 88.3710 },
    { name: "Bidhan Nagar", lat: 22.5915, lon: 88.3908 },
    { name: "Dharmatala", lat: 22.5601, lon: 88.3525 },
    { name: "Shobhabazar", lat: 22.5982, lon: 88.3640 },
    { name: "Newtown", lat: 22.5754, lon: 88.4798 },
    { name: "Salt Lake Sector V", lat: 22.5809, lon: 88.4291 },
  ]

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.watchPosition((position) => {
        const { longitude, latitude } = position.coords;
        setLon(longitude);
        setLat(latitude);
      })
    }
  }, []);

  if (!lat || !lon) {
    return <h1>Loading...</h1>;
  }

  const setDestination = (name, lat, lon) => {
    console.log(name);
    setDestinationData({lat, lon, name});
  }

  return (
    <MapContainer center={[22.5744, 88.3629]} zoom={14} scrollWheelZoom={false}>
      <TileLayer attribution='<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
        url="https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=xpL7wNLWmyhEZZoEtLXq" />

      {/* <ChangeView center={[lat, lon]} /> */}
      <ChangeView center={[22.5744, 88.3629]} />

      <CircleMarker center={[22.5744, 88.3629]} radius={10} color='transparent' fillColor='blue' opacity={5}>
        <Popup>
          <h1>Kolkata</h1>
        </Popup>
      </CircleMarker>

      <Marker position={[22.5744, 88.3629]}>
        <Popup>
          <h1 className="text-xs">My Location</h1>
        </Popup>
      </Marker>

      {parkingLocations.length !== 0 && (
        parkingLocations.map((data) =>
          <Marker key={data.name} position={[data.lat, data.lon]} eventHandlers={{click: () => setDestination(data.name, data.lat, data.lon)}}>
            <Popup>
              <h1>{data.name}</h1>
            </Popup>
          </Marker>
        )
      )}

      {destinationData && (
        // <Routing lat={lat} lon={lon} destinationData={destinationData} />
        <Routing lat={22.5744} lon={88.3629} destinationData={destinationData} />
      )}
    </MapContainer>
  )
}
