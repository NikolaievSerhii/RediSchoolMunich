from http.server import BaseHTTPRequestHandler, HTTPServer
import database as db

class MyServer(BaseHTTPRequestHandler):
    # Вернем страничку с данными из базы, в дальнейшем дописать пареметры гет и пос зарпосов и ставить фильтры
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Base </title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))

        base = db.Database()
        base.connect()

        all_users = base.query('select * from file_result')
        date = str("<table border = 1px ><tr ALIGN=right><th>amount</th><th>use</th><th>change</th><th>payment</th><th>fee</th><th>File</th><th>Terminal</th><th></th></tr>")
        for stroka in all_users:
            date += '<tr ALIGN=right>'
            for el in stroka:
                if (el == 'Error'):
                    date += '<th BGCOLOR=red>' + str(el) + '</th>'
                else:
                    date += '<th>' + str(el) + '</th>'
            date += '</tr>'
        date += '</table>'
        base.close()

        self.wfile.write(bytes(date,  'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))


