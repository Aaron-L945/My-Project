import hashlib
from random import randint

import pymysql
import time

from os import remove
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options
from tornado.web import Application, RequestHandler, UIModule


#tornadodb
from day4.util.dbutil import DBUtil
from day4.util.myutil import mymd5

#tornadoapp
from day5.app import mysettings
from day5.app.app import MyApplication
from day5.app.myhandlers import IndexHandler, LoginHandler, BlogHandler, RegistHandler, CheckHandler
from day5.app.mymodules import LoginModule, BlogModule, RegistModule

app = MyApplication([('/',IndexHandler),
                   ('/login',LoginHandler),
                   ('/blog',BlogHandler,{'date':'0408','subject':'tornadoresp'}),
                   ('/regist', RegistHandler),
                     ('/check',CheckHandler)
                   ],
                  tp='mytemplate',
                  sp='mystatics',
                  ui={'loginmodule':LoginModule,'blogmodule':BlogModule,'registmodule':RegistModule})
server = HTTPServer(app)
server.listen(mysettings.settings.get('port',8888))#3 读取配置文件中的端口号
IOLoop.current().start()