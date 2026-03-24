require("dotenv").config();
const express = require("express");
const cors = require("cors");
const rateLimit = require("express-rate-limit");

const connectDB = require("./config/dbConfig");
const extractData = require("./utils/extractData");
const metroRouter = require("./routes/metroRouter");
const alFatahRouter = require("./routes/alFatahRouter");
const featuredRouter = require("./routes/featuredRouter");
const jalalSonsRouter = require("./routes/jalalSonsRouter");
const rajaSahibRouter = require("./routes/rajaSahibRouter");
const rahimStoreRouter = require("./routes/rahimStoreRouter");
const productMatchesRouter = require("./routes/productMatchesRouter");
const searchRouter = require("./routes/searchRouter");

const app = express();

// Rate limiting configuration
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: "Too many requests from this IP, please try again later.",
  standardHeaders: true,
  legacyHeaders: false,
});

// Apply rate limiting to all routes
app.use(limiter);

// CORS configuration
const allowedOrigins = [
  "http://localhost:5173",
  "https://grocy-02c9.onrender.com",
];

app.use(
  cors({
    origin: function (origin, callback) {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error("Not allowed by CORS"));
      }
    },
    credentials: true,
  }),
);

const PORT = process.env.PORT || 8000;

connectDB().then(() => {
  // extractData("./scrapped data/Metro.csv", "metro");
  // extractData("./scrapped data/Al-Fatah.csv", "alFatah");
  // extractData("./scrapped data/Jalal Sons.csv", "jalalSons");
  // extractData("./scrapped data/Raja Sahib.csv", "rajaSahib");
  // extractData("./scrapped data/Rahim Store.csv", "rahimStore");

  app.use("/metro", metroRouter);
  app.use("/search", searchRouter);
  app.use("/alfatah", alFatahRouter);
  app.use("/featured", featuredRouter);
  app.use("/jalalsons", jalalSonsRouter);
  app.use("/rajasahib", rajaSahibRouter);
  app.use("/rahimstore", rahimStoreRouter);
  app.use("/matches", productMatchesRouter);

  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    console.log("Fresh deployment")
  });
});
