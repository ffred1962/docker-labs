from pathlib import Path

def get_file(path):
   mime = "text/plain"

   if path.endswith(".css"):
       mime = "text/css"
   elif path.endswith(".html"):
       mime = "text/html"
   elif path.endswith(".js"):
       mime = "text/javascript"

   code = 200

   file_name = Path(path).name
   text = ""
   if ".." in path:
       text = "unauthorized: unable to traverse outside of main directory"
       code = 401
   else:
       try:
           with open("./function/homepage/static" + file_name) as f:
               text = f.read()
       except:
           text = "not found"

   return code, text, mime

def handle(event, context):
   path = event.path
   if path == "/" or path =="":
       path = "/index.html"
   code, text, mime = get_file(path)

   return {
       "statusCode": code,
       "body": text,
       "headers": {
           "Content-type": mime
       }
   }

