from flask import send_file, request,render_template, current_app
from flask.ext.restful import Resource, Api
from utils.app_ctx import ApplicationContext

def get_image(art_id, action_type):
    app_ctx =ApplicationContext('art')
    item = app_ctx.get_item(art_id)
    if action_type=='view':
        return render_template('artView.html',art=item)
    imagedir = current_app.config['UPLOAD_FOLDER']
    extension = 'png'

    if action_type=="thumbnail":
        fn = "%s/%s_tn.%s" % (imagedir, art_id, extension)
    if action_type=="picture":
        fn = "%s/%s.%s" % (imagedir, art_id, extension)
    if action_type=="qrcode":
        fn = '%s/%s_qr.png' % (imagedir, art_id)

    # Set the right return MIME type
    returnMime = 'image/png'
    ext = fn.split(".")[1].lower()
    if ext == 'jpg': returnMime = 'image/jpeg'
    return send_file(fn, mimetype=returnMime)