import ParkingSpotModel from "../models/parkingSpot.model.js";
import PricingModel from "../models/Pricing.model.js";
import { errorHandeler } from "../utils/error.js";

export const addSpot = async (req, res, next) => {
    if(req.user._id !== req.params.userId) return next(errorHandeler(401, "User Missmatch please login to your own account"));

    try{
        const newSpot = await ParkingSpotModel.create(req.body);
        return res.status(201).json(newSpot);
    }catch(error){
        next(error);
    }
};

export const addPricing = async (req, res, next) => {
    const parkingSpot = await ParkingSpotModel.findById(req.params.spotId);

    if(!parkingSpot) return next(errorHandeler(404, "Paking spot not found"));

    if(req.user._id !== parkingSpot.userRef) return next(errorHandeler(401, "You can only update your own spots"));

    try{
        const pricingArray = req.body;
        // store all the pricing Ids
        const pricingIds = await Promise.all(
            pricingArray.map(async (pricing) => {
                const newPricing = new PricingModel(pricing);
                await newPricing.save();
                return newPricing._id;
            })
        );

        const updatedParkingspot = await ParkingSpotModel.findByIdAndUpdate(
            req.params.spotId,
            { pricing: pricingIds }, //only updating the pricing
            {new: true}
        );

        res.status(200).json(updatedParkingspot);
    }catch(error){
        next(error);
    }
};

export const spotDetails = async (req, res, next) => {
    try{
        const spotData = await ParkingSpotModel.findById(req.params.spotId).populate("pricing");
        if(!spotData) return next(errorHandeler(404, "Parking Spot not found"));
        return res.status(200).json(spotData);
    }catch(error){
        next(error);
    }
};

export const allSpotData = async (req, res, next) => {
    try{
        const allParkingSpot = await ParkingSpotModel.find().populate("pricing");
        if(!allParkingSpot) return next(errorHandeler(404, "No Parking Spot available"));
        return res.status(200).json(allParkingSpot);
    }catch(error){
        next(error);
    }
}