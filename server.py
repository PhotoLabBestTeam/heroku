import subprocess

import web

urls = (
    '/', 'index'
)

render = web.template.render('templates/')
str = "#"


class index:
    def GET(self):
        f = open("out.txt", "r")
        str = f.read()
        print(str)
        f.close()
        if str is None or len(str) < 1:
            str = "http://placehold.it/300x400"
        str1 = None
        f1 = open("in.txt", "r")
        str1 = f1.read()
        f1.close()
        if str1 is None or len(str1) < 1:
            str1 = "http://placehold.it/300x400"
        return render.index(str, str1)

    def POST(self):
        x = web.input(myfile={})
        filedir = 'static'  # change this to the directory you want to store the file in.
        if 'myfile' in x:  # to check if the file-object is created
            filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + filename, 'w')  # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.
        f1 = open("in.txt", "w+")
        f1.write(filedir + '/' + filename)
        f1.close()

        subprocess.call("bash script.sh " + filedir + '/' + filename, shell=True)

        raise web.seeother('/')


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()