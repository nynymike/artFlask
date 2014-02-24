from flask import send_file, request,render_template, current_app
from flask.ext.restful import Resource, Api
from utils.helpers import  upload_file, jsonify
from utils.app_ctx import ApplicationContext
from bson import json_util
import io

class ArtImage(Resource):

    def get(self,art_id,action_type):
		app_ctx =ApplicationContext('art')
		item = app_ctx.get_item(art_id)
		if action_type=='view':
			return render_template('artView.html',art=item)
		imagedir = current_app.config['UPLOAD_FOLDER']
		extension = 'png'
		if action_type=="thumbnail":
			fn = "%s/thumb-%s.%s"%(imagedir,art_id,extension)
		if action_type=="picture":
			fn = "%s/web-%s.%s"%(current_app.config['UPLOAD_FOLDER'],art_id,extension)
		if action_type=="qrcode":
			fn = '%s/qrcode.png' % (imagedir)
		return  send_file(fn, mimetype='image/png')