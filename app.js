/* 
 * Dependencies
 */
var express = require('express'),
  path = require('path'),
  fs = require('fs'),
  http = require('http'),
  exphbs = require('express3-handlebars'),
  lessMiddleware = require('less-middleware'),
  _ = require("underscore"),
  yhat = require('yhat');


yh = yhat.init(process.env.YHAT_USERNAME, process.env.YHAT_APIKEY, "http://cloud.yhathq.com/");


var examples = [
  {
    "account_length": 128,
    "area_code": 487,
    "intl_plan": "no",
    "vmail_plan": "yes",
    "vmail_message": 25,
    "day_mins": 265,
    "day_calls": 110,
    "day_charge": 45,
    "eve_minutes": 197.4,
    "eve_calls": 99,
    "eve_charge": 16.7,
    "night_mins": 244.7,
    "night_calls": 91,
    "night_charge": 11,
    "intl_mins": 10,
    "intl_calls": 3,
    "intl_charge": 2.7,
    "custserv_calls": 1
  }
]

/*
 * Initiate Express
 */
var app = express();


/* 
 * App Configurations
 */
app.configure(function() {
  app.set('port', process.env.PORT || 5000);

  app.set('views', __dirname + '/views');

  app.set('view engine', 'html');
  app.engine('html', exphbs({
    defaultLayout: 'main',
    extname: '.html'
    //helpers: helpers
  }));
  app.enable('view cache');

  app.use(lessMiddleware({
    src: __dirname + '/public',
    compress: true,
    sourceMap: true
  }));
  app.use(express.static(path.join(__dirname, 'public')));

  app.use(express.bodyParser());
  app.use(express.favicon());
  app.use(express.logger('dev')); 
  app.use(express.methodOverride());
  app.use(app.router);
});

app.configure('development', function(){
  app.use(express.errorHandler());
});

/*
* Route for Index
*/
app.get('/', function(req, res) {
  var idx = Math.floor(Math.random()*1);
  res.render('index', { params: examples[idx] });
});

app.post('/', function(req, res) {
  data = req.body;
  _.map(_.keys(data), function(k) {
    data[k] = [data[k]];
  });
  yh.predict("PythonChurnModel", data, function(err, result) {
    res.send(result);
  });
});


/*
 * Routes for Robots/404
 */
app.get('/robots.txt', function(req, res) {
  fs.readFile(__dirname + "/robots.txt", function(err, data) {
    res.header('Content-Type', 'text/plain');
    res.send(data);
  });
});

app.get('*', function(req, res) {
  res.render('404');
});


http.createServer(app).listen(app.get('port'), function() {
  console.log("Express server listening on port " + app.get('port'));
});
