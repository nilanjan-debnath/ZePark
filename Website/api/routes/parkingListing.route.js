import express from "express";
import { addSpot, addPricing, spotDetails, allSpotData } from "../controllers/parkingListing.controller.js";
import { verifyToken } from "../utils/verifyUser.js";

const router = express.Router();

router.post("/addSpot/:userId", verifyToken, addSpot);
router.post("/addPricing/:spotId", verifyToken, addPricing);
router.get("/spotDetails/:spotId", verifyToken, spotDetails);
router.get("/allSpotData", verifyToken, allSpotData);

export default router;