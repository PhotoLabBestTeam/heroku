import subprocess

import web

urls = (
    '/', 'index',
    '/result', 'result',
    '/favicon.ico', 'icon'
)
render = web.template.render('templates/')

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session

class index:
    def GET(self):
        return render.index()

    def POST(self):
        x = web.input(input_img={})
        filedir = 'static/session_imgs'

        assert 'input_img' in x
        filename = session.session_id
        fout = open(filedir + '/' + filename, 'w')
        fout.write(x.input_img.file.read())
        fout.close()

        after = subprocess.check_output(["bash", "script.sh", filedir + '/' + filename])
        session['before'] = filedir + '/' + filename
        session['after'] = after
        raise web.seeother('/result')


class result:
    def GET(self):
        return render.result(session['before'], session['after'])

    def POST(self):
        x = web.input(input_img={})
        filedir = 'static/session_imgs'

        assert 'input_img' in x
        filename = session.session_id
        fout = open(filedir + '/' + filename, 'w')
        fout.write(x.input_img.file.read())
        fout.close()

        after = subprocess.check_output(["bash", "script.sh", filedir + '/' + filename])
        session['before'] = filedir + '/' + filename
        session['after'] = after

        return render.result(session['before'], session['after'])


class icon:
    def GET(self):
        raise web.seeother("/static/favicon.ico")


if __name__ == "__main__":
    app.run()