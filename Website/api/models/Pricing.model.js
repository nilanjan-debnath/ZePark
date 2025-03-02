import mongoose from "mongoose";

const pricingSchema = new mongoose.Schema({
    price: {
        type: Number,
        required: true,
    },
    time: {
        type: Number,
        required: true,
    },
    pro: {
        type: Boolean,
        default: false,
    },
});

const Pricing = mongoose.model('pricing', pricingSchema);

export default Pricing;