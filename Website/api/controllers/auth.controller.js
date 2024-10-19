import bcryptjs from "bcryptjs";
import userModel from "../models/user.model.js";
import { errorHandeler } from "../utils/error.js";

export const signUp = async (req, res, next) => {
    const {username, email, password, contact} = req.body;
    if(!username || !email || !password || !contact){
        return next(errorHandeler(404, "Missing Credentials"));
    }
    const hashedPassword = bcryptjs.hashSync(password, 10);
    const newUser = new userModel({username, email, password: hashedPassword, contact});
    try{
        await newUser.save();
        res.status(201).json("User created successfully");
    }catch(error){
        next(error);
    }
}