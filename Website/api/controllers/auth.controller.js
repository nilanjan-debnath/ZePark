import bcryptjs from "bcryptjs";
import userModel from "../models/user.model.js";
import { errorHandeler } from "../utils/error.js";
import jwt from "jsonwebtoken";

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
};

export const signIn = async (req, res, next) => {
    const {email, password} = req.body;
    if(!email || !password){
        return next(errorHandeler(404, "Missing Credentials"));
    }
    try{
        const validUser = await userModel.findOne({email});
        if(!validUser) return next(errorHandeler(404, "User not found"));
        const validPassword = bcryptjs.compareSync(password, validUser.password);
        if(!validPassword) return next(errorHandeler(401, "Wrong Credentials"));
        const token = jwt.sign({_id: validUser._id, email: validUser.email, username: validUser.username, contact: validUser.contact, avatar: validUser.avatar}, process.env.JWT_SECRECT);
        const {password: pass, ...rest} = validUser._doc;
        res.cookie('zepark_token', token, {httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000}).status(200).json(rest);
    }catch(error){
        next(error);
    }
}