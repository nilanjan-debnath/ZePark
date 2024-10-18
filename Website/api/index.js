import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";
import authRouter from "./routes/auth.route.js";

dotenv.config();

mongoose.connect(process.env.MONGO).then(() => {
    console.log("mongodb connected successfully");
}).catch((error) => {
    console.log(error);
})

const app = express();

app.use(express.json());

app.listen(3000, () => {
    console.log("server is running at port 3000");
});

// created routers
app.use("/api/auth", authRouter);


app.use((err, req, res, next) => {
    const statusCode = err.statusCode || 500;
    const message = err.message || "Internal Server Error";
    return res.status(statusCode).json({
        success: false,    
        statusCode,
        message,
    });
});