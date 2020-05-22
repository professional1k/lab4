# py_ver == "3.6.9"
import flask


app = flask.Flask(__name__)


@app.route("/colour")
def set_colour():
    return """
            <html>
            <script>
            window.changeColour = function() {
            document.body.style.backgroundColor = location.hash.replace('#', '');
            document.getElementsByName("text")[0].innerHTML = decodeURI(location.hash.replace('#', ''));
            }
            </script>
            <body>
            <p name="text"></p>
            <div style="height:100vh" onmousemove=changeColour()></div>
            </body>
            </html>
            """


import requests
@app.route('/parser', methods=['GET', 'POST'])
def parse_list():
    if flask.request.method == 'POST':
        if 'file' not in flask.request.files:
            return flask.redirect(flask.request.url)
        file = flask.request.files['file']
        if file.filename == '':
            return flask.redirect(flask.request.url)
        if file and file.filename.endswith(".xml"):
            from xml.dom import pulldom
            parser = pulldom.parse(file)
            for node in parser:
                data = node[1]
                parser.expandNode(data)
                requests.post("https://storage.mainfraim.ecc/save_data", data=data.toxml())
    return flask.redirect('/load_xml')


@app.route('/load_xml')
def loader():
    return """
    <html>
      <body>
        <h2>Загрузите XML-документ для обработки</h2>
        <form action="/parser" method="post" enctype="multipart/form-data">
          <input name="file" type="file">
          <input name="submit" type="submit" value="Загрузить">
        </form>
      </body>
    </html>
    """


if __name__ == '__main__':
    app.run()
