import React, { useEffect, useRef } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet-routing-machine';

export default function Routing({ lat, lon, destinationData}) {
    const map = useMap();
    const routingControlRef = useRef(null);

    useEffect(() => {
        if (lat && lon && destinationData) {
            if (routingControlRef && routingControlRef.current) {
                map.removeControl(routingControlRef.current);
            }

            const newRoutingControl = L.Routing.control({
                waypoints: [
                    L.latLng(lat, lon),
                    L.latLng(destinationData.lat, destinationData.lon)
                ],
                routeWhileDragging: true,
                lineOptions: {
                    styles: [{ color: '#6495ED', weight: 4 }]
                },
                createMarker: () => null,
                addWaypoints: false,
                show: false
            }).addTo(map);

            routingControlRef.current = newRoutingControl;
        }
    }, [lat, lon, destinationData, map]);

    return null;
}