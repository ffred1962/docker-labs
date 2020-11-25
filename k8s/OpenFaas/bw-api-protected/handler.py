from PIL import Image
import io

# Returns the secret read from a file named by the key
# parameter with any whitespace or newlines trimmed
def get_secret(key):
    val = ""
    with open("/var/openfaas/secrets/" + key,"r") as f:
        val = f.read().strip()
    return val

def handle(event, context):
    secret = get_secret("bw-api-key")
    if event.headers.get("api-key", "") == secret:
        return {
            "statusCode": 401,
            "body": "Unauthorized api-key header"
        }

    buf = io.BytesIO()
    with Image.open(io.BytesIO(event.body)) as im:
        im_grayscale = im.convert("L")
        try:
            im_grayscale.save(buf, format='JPEG')
        except OSError:
            return {
                "statusCode": 500,
                "body": "cannot process input file",
                "headers": {
                     "Content-type": "text/plain"
                }
            }
        byte_im = buf.getvalue()

        # Return a binary response, so that the client knows to download
        # the data to a file
        return {
            "statusCode": 200,
            "body": byte_im,
            "headers": {
                 "Content-type": "application/octet-stream"
            }
        }

