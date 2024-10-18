import bcryptjs from "bcryptjs";
import userModel from "../models/user.model.js";

export const signUp = async (req, res, next) => {
    const {username, email, password, contact} = req.body;
    console.log(username, email, password, contact)
    const hashedPassword = bcryptjs.hashSync(password, 10);
    const newUser = new userModel({username, email, password: hashedPassword, contact});
    try{
        await newUser.save();
        res.status(201).json("User created successfully");
    }catch(error){
        next(error);
    }
}