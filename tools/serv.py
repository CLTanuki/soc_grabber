__author__ = 'mFoxRU'
from flask import Flask
from db_work.models import TwitterUser, VkUser

app = Flask(__name__)


@app.route("/")
def status():
    return 'Daemon is up and running...'


@app.route("/tweet")
def tweet():
    user_count = TwitterUser.select().count()
    ru_user_count = TwitterUser.select(TwitterUser.is_ru is True).count()
    reply = ('В базе %s пользователей. \
              Из них %s русскоязычных.') % (user_count, ru_user_count)
    return reply


@app.route("/vk")
def vk():
    user_count = VkUser.select().count()
    ru_user_count = VkUser.select(VkUser.is_ru is True).count()
    reply = ('В базе %s пользователей. \
              Из них %s русскоязычных.') % (user_count, ru_user_count)
    return reply

if __name__ == "__main__":
    app.run(debug=True)
