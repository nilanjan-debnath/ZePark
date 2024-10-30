import mongoose from "mongoose";

const parkingSpotSchema = new mongoose.Schema({
    ownerName: {
        type: String,
        required: true,
    },
    name: {
        type: String,
        unique: true,
        required: true
    },
    contact: {
        type: String,
        unique: true,
        required: true
    },
    rating: [{
        type: Number,
    }],
    latitude: {
        type: Number,
        required: true,
    },
    longitude: {
        type: Number,
        required: true,
    },
    pricing: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'pricing',
    }],
    address: {
        type: String,
        required: true,
    },
    totalSlot: {
        type: Number,
        required: true,
    },
    userRef: {
        type: String,
        required: true
    }
}, {timestamps: true});

const ParkingSpot = mongoose.model('parkingSpot', parkingSpotSchema);
export default ParkingSpot;