# Churn Prediction Demo

### Quickstart
##### Deployment
```bash
$ git clone https://github.com/yhat/demo-churn-pred/
$ cd model
$ python churn_model.py
```
##### App
```bash
$ cd demo-churn-pred
$ export YHAT_USERNAME=foo
$ export YHAT_APIKEY=abcd1234
$ node app.js
```

### Model
To deploy the model on ScienceOps, clone this repo (`git clone https://github.com/yhat/demo-churn-pred`), or download the [`churn.csv`](https://raw.githubusercontent.com/yhat/demo-churn-pred/master/model/churn.csv) and [`chrun_model.py`](https://raw.githubusercontent.com/yhat/demo-churn-pred/master/model/churn_model.py) files.

Put them in the same folder and run `python churn_model.py`. You'll be prompted for your ScienceOps username and apikey. If you don't already have credentials, you can get them here: https://yhathq.com/signup.
