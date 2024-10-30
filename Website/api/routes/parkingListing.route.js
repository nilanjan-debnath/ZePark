import express from "express";
import { addSpot, addPricing } from "../controllers/parkingListing.controller.js";
import { verifyToken } from "../utils/verifyUser.js";

const router = express.Router();

router.post("/addSpot/:userId", verifyToken, addSpot);
router.post("/addPricing/:spotId", verifyToken, addPricing);

export default router;