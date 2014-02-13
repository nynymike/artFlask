from model.Art import ArtWork
from utils.helpers import request_to_dictonary, update_from_dictionary
from flask import request

MODEL_MAP = {
			"art" : ArtWork
} 

class ApplicationContext(object):



	def __init__(self,model_name):
		self.model_name = model_name

	def create_item_from_context(self):
		model_class = self.model_class()
		item = model_class()
		data = request_to_dictonary(model_class)
		update_from_dictionary(data,item,model_class)

	def model_class(self):
		return MODEL_MAP[self.model_name]






