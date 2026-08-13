const express = require('express');
const router = express.Router();
const controllers = require('../controllers/controllers');

router.get('/', controllers.index);
router.get('/postcard', controllers.postcard);
router.get('/destinations', controllers.destinations);
router.post('/report', controllers.report);

module.exports = router;