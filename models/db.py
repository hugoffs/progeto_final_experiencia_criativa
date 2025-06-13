from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

instance = "mysql+pymysql://ldevs:ldevs@localhost:3306/ldev_sprinkler"
#instance = "mysql+pymysql://ldevs:Ldevs2024!@localhost:3306/ldev_sprinkler"        # meu not não aceitou a cenha kkkkkkkkk
