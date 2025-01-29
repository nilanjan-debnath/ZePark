import express from "express";
import { verifyToken } from "../utils/verifyUser.js";
import {readToken} from "../controllers/user.controller.js";

const router = express.Router();

router.get("/readToken",verifyToken, readToken);

export default router;