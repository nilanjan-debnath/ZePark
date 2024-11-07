import express from "express";
import { signUp, signIn, logout } from "../controllers/auth.controller.js";

const router = express.Router();

router.post("/signup", signUp);
router.post("/signin", signIn);
router.get("/logout", logout);

export default router;