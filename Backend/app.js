require("dotenv").config();
const express = require("express");
const cors = require("cors");

const app = express();

app.use(
  cors({
    origin: "http://localhost:5173",
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true,
  })
);

const connectDB = require("./config/dbConfig");

const extractData = require("./utils/extractData");

const metroRouter = require("./routes/metroRouter");
const alFatahRouter = require("./routes/alFatahRouter");
const jalalSonsRouter = require("./routes/jalalSonsRouter");
const rajaSahibRouter = require("./routes/rajaSahibRouter");
const rahimStoreRouter = require("./routes/rahimStoreRouter");

const PORT = process.env.PORT || 8000;

connectDB();
// extractData("./scrapped data/Metro.csv", "metro");
// extractData("./scrapped data/Al-Fatah.csv", "alFatah");
// extractData("./scrapped data/Jalal Sons.csv", "jalalSons");
// extractData("./scrapped data/Raja Sahib.csv", "rajaSahib");
// extractData("./scrapped data/Rahim Store.csv", "rahimStore");

app.use("/metro", metroRouter);
app.use("/alfatah", alFatahRouter);
app.use("/jalalsons", jalalSonsRouter);
app.use("/rajasahib", rajaSahibRouter);
app.use("/rahimstore", rahimStoreRouter);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
