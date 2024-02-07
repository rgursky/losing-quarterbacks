const express = require('express');
const router = express.Router();

const QB = require('../../models/QBs');

// @route GET api/qbs/test
// @desc Tests qbs route
// @access Public
router.get('/test', (req, res) => res.send('QB route testing!'));

// @route GET api/qbs
// @desc Get all qbs
// @access Public
router.get('/', (req, res) => {
    QB.find()
        .then(qb_record => res.json(qb_record))
        .catch(err => res.sendStatus(404).json({noqbsfound: 'No QBs found'}));
});


// @route GET api/qbs/:losers
// @desc Get all qbs with losing record that lost sb
// @access Public
router.get('/losers', async (req, res) => {
    try {
        const result = await QB.aggregate([
            {
              $lookup: {
                from: "lost_sb_with_losing_record",
                localField: "Name",
                foreignField: "Name",
                as: "matched_docs",
              },
            },
            {
              $match: {
                matched_docs: { $ne: [] },
              },
            }
        ]);
        res.json(result);
    } catch(err) {
        console.error(err);
        res.status(500).send("Internal server error");
    }
});

// @route GET api/qbs/:winners
// @desc Get all qbs with winning record that won sb
// @access Public
router.get('/winners', async (req, res) => {
    try {
        const result = await QB.aggregate([
            {
              $lookup: {
                from: "won_sb_with_losing_record",
                localField: "Name",
                foreignField: "Name",
                as: "matched_docs",
              },
            },
            {
              $match: {
                matched_docs: { $ne: [] },
              },
            }
        ]);
        res.json(result);
    } catch(err) {
        console.error(err);
        res.status(500).send("Internal server error");
    }
});

module.exports = router;