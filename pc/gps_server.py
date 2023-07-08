import falcon, json
from wsgiref.simple_server import make_server


class DownloadGpsLog(object):
  companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
  resp_ok = {"status":"ok"}
  def on_post(self, req, resp):
    js=req.bounded_stream.read()
    print(f"raw={js}")
    content=json.loads(js)
    print(f"decoded={content}")
    for item in content:
       fname=item["filename"]
       lines=item["content"]
       with open(fname, "a") as fh:
          for line in lines:
             fh.write(line)
    resp.body = json.dumps(self.resp_ok)



app = falcon.App()
gps = DownloadGpsLog()
app.add_route('/gps', gps)
with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
