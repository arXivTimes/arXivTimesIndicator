# arXivTimesIndicator
Indicator Dashboard for arXivTimes


## Installation

Store Twitter keys to environmental variables:
```shell
export CONSUMER_KEY=xxx
export CONSUMER_SECRET=xxx
export ACCESS_TOKEN=xxx
export ACCESS_TOKEN_SECRET=xxx
```

Clone this repository and setup virtualenv:

```shell
$ git clone https://github.com/chakki-works/arXivTimesIndicator.git
$ cd arXivTimesIndicator
$ virtualenv venv --python=python3
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Write cron setup to /etc/crontab:
```shell
sudo apt-get install -y cron
sudo touch /var/log/indicator.log
sudo sh -c 'echo "24 0 * * * root /home/ubuntu/hoge/run_crawler.sh > /var/log/indicator.log 2>&1" >> /etc/crontab'
```