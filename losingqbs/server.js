const express = require('express');
const connectDB = require('./config/db');
const routes = require("./routes/api/qbs");
const path = require("path");
const cors = require("cors");
const bodyParser = require("body-parser");

const server = express();

server.use(cors({ origin: true, credentials: true }));
// server.use(express.json({ extended: false }));
server.use(bodyParser.json());
server.use(bodyParser.urlencoded({ extended: true }));
server.use("/api/qbs", routes);

connectDB();

const port = process.env.PORT || 8082;

server.listen(port, () => console.log(`Server running on port ${port}`));