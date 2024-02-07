const mongoose = require('mongoose');

const QBSchema = new mongoose.Schema({
    "_id": {
        type: String //mongoose.Schema.Types.ObjectId
    },
    "Name": {
        type: String,
        required: true
    },
    "W-L-T": {
        type: String
    },
    "Percentage": {
        type: String
    },
    "Won_Lost_Superbowl": {
        type: String
    }},
    { collection : 'qb_records'}
);

module.exports = QB = mongoose.model('qb_record', QBSchema, 'qb_records');