import React from 'react';
import { MapContainer, CircleMarker, Marker, Popup, TileLayer, useMap } from "react-leaflet";

import 'leaflet/dist/leaflet.css'

export default function Map() {
  return (
    <MapContainer center={[22.5744, 88.3629]} zoom={13} scrollWheelZoom={false}>
      <TileLayer attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      <CircleMarker center={[22.5744, 88.3629]} radius={10} color='transparent' fillColor='blue' opacity={5}>
        <Popup>
          <h1>Kolkata</h1>
        </Popup>
      </CircleMarker>

      <Marker position={[22.5754, 88.4798]}>
        <Popup>
          <h1>New Town</h1>
        </Popup>
      </Marker>
    </MapContainer>
  )
}
