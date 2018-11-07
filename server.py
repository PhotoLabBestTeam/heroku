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
    '/favicon.ico', 'icon'
)
render = web.template.render('templates/')

app = web.application(urls, globals())

#web.config.session_parameters.timeout = 600
#web.config.session_parameters.ignore_expiry = False
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'before': '/static/PhLab1.jpg', 'after': '/static/PhLab1.jpg'})
    web.config._session = session
else:
    session = web.config._session

class index:
    def GET(self):
        return render.index()

class filters:
    def GET(self):
        return render.filters()

class result:
    def GET(self, name):
        return web.seeother("callback:nativePhotoSelect?func=alert('e')")
        return render.result(session['before'], session['after'], "hidden")

    def POST(self, name):
        x = web.input(input_img={})
        filedir = 'static/session_imgs'

        assert 'input_img' in x
        filename = session.session_id
        path = filedir + '/' + filename
        fout = open(path, 'w')
        fout.write(x.input_img.file.read())
        fout.close()

        session['before'] = subprocess.check_output(["bash", "get_url.sh", path])
        os.remove(path)
        #os.remove('sessions/' + filename)
        after = subprocess.check_output(["bash", "script.sh", session['before'], name])
        if after.startswith('http'):
            session['after'] = after
        else:
            session['after'] = '/static/PhLab1.jpg'

        before = session['before']
        after = session['after']
        session.kill()
        return render.result(before, after, "")


class icon:
    def GET(self):
        raise web.seeother("/static/favicon.ico")


if __name__ == "__main__":
    app.run()