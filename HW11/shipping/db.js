const mongoose = require("mongoose");

const connectDB = async () => {
    try {
        await mongoose.connect("mongodb://localhost:27017/shipping", {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        console.log("MongoDB connected for shipping service");
    } catch (err) {
        console.error("DB connection error:", err.message);
        process.exit(1);
    }
};

module.exports = connectDB;