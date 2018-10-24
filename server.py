import subprocess

import web

urls = (
    '/', 'index',
    '/result', 'result'
)
render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index()

    def POST(self):
        x = web.input(input_img={})
        filedir = 'static'

        assert 'input_img' in x
        filepath = x.input_img.filename.replace('\\', '/')
        filename = filepath.split('/')[-1]
        fout = open(filedir + '/' + filename, 'w')
        fout.write(x.input_img.file.read())
        fout.close()

        f1 = open("in.txt", "w+")
        f1.write(filedir + '/' + filename)
        f1.close()

        subprocess.call("bash script.sh " + filedir + '/' + filename, shell=True)

        raise web.seeother('/result')


class result:
    def GET(self):
        f = open("out.txt", "r")
        after = f.read()
        f.close()
        if after is None or len(after) < 1:
            after = "http://placehold.it/300x400"
        f1 = open("in.txt", "r")
        before = f1.read()
        f1.close()
        if before is None or len(before) < 1:
            before = "http://placehold.it/300x400"
        return render.result(before, after)

    def POST(self):
        x = web.input(input_img={})
        filedir = 'static'  # change this to the directory you want to store the file in.
        if 'input_img' in x:  # to check if the file-object is created
            filepath = x.input_img.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + filename, 'w')  # creates the file where the uploaded file should be stored
            fout.write(x.input_img.file.read())  # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.
        f1 = open("in.txt", "w+")
        f1.write(filedir + '/' + filename)
        before = filedir + '/' + filename
        f1.close()

        after = subprocess.check_output(["bash", "script.sh",  filedir + '/' + filename])

        return render.result(before, after)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()