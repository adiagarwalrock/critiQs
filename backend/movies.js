const axios = require('axios');
const express = require('express');
const router = express.Router();

var HOME_PAGE_API = 'http://127.0.0.1:8000/movie/top_rated/';



router.get('/', async (req, res) => {
    try {
        const response = await axios.get(HOME_PAGE_API);
        res.send(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});


module.exports = router;
