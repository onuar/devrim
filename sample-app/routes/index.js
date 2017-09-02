var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
  var waitingTime = Math.floor(Math.random() * 5) + 1;
  setTimeout(function () {
    res.render('index', { message: 'Sleeping time: ' + waitingTime });
  }, waitingTime * 1000);

});

module.exports = router;
