import subprocess

import web
import os
import os.path
import time

# class MyDiskStore(web.session.DiskStore):
#     def cleanup(self, timeout):
#         now = time.time()
#         for f in os.listdir(self.root):
#             path = self._get_path(f)
#             atime = os.stat(path).st_atime
#             if now - atime > timeout :
#                 os.remove(path)
#                 img_path = 'static/session_imgs/' + path.split("/")[-1]
#                 if os.path.isfile(img_path):
#                     os.remove(img_path)

urls = (
    '/', 'index',
    '/result(.+)', 'result',
    '/filters', 'filters',
    '/process(.+)', 'process',
    '/final', 'final',
    '/favicon.ico', 'icon'
)
render = web.template.render('templates/')

app = web.application(urls, globals())

#web.config.session_parameters.timeout = 600
#web.config.session_parameters.ignore_expiry = False
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'select': False, 'name': '', 'before': '/static/PhLab1.jpg', 'after': '/static/PhLab1.jpg'})
    web.config._session = session
else:
    session = web.config._session


class index:
    def GET(self):
        if session['select']:
            session['select'] = False
            return render.result(session['name'])
        return render.index()

class filters:
    def GET(self):
        return render.filters()

class result:
    def GET(self, name):
        session['name'] = name
        session['select'] = True
        return web.seeother('/')

class process:
    def GET(self, url):
        url = "http://" + url
        session['before'] = url
        return render.process("", "", "hidden", "", 'true')

class final:
    def GET(self):
        after = subprocess.check_output(["bash", "script.sh", session['before'], session['name']])
        if not after.startswith('http'):
            after = '/static/PhLab1.jpg'
        session['after'] = after
        return render.process(session['before'], session['after'], "", "hidden" 'false')

class icon:
    def GET(self):
        raise web.seeother("/static/favicon.ico")


if __name__ == "__main__":
    app.run()