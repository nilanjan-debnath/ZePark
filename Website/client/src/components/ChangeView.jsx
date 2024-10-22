import React, { useEffect } from 'react'
import {useMap } from 'react-leaflet';

export default function ChangeView({center}) {

    const map = useMap();

    useEffect(() => {
        if(center[0] !== 0 || center[1] !== 0){
            map.setView(center, map.getZoom());
        }
    }, [center, map]);

  return null;
}
