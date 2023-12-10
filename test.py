import pymysql
import configparser

config = configparser.ConfigParser()
config.read('conf/config.ini')
host = config["MYSQL"]['remote_host']
user = config["MYSQL"]['user']
password = config["MYSQL"]['password']
port = int(config["MYSQL"]['port'])
#print(host)
_client = pymysql.connect(host="db-1trvs-kr1.vpc-cdb.gov-ntruss.com", port=3306,
                          user=user, password=password,db='flowbit')