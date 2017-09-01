var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  
  setTimeout(function() {
    res.render('index', { title: 'Express' });  
  }, 0);
  
});

module.exports = router;
