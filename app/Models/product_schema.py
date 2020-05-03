from mongoengine import *
from flask import jsonify


class Product(Document):

    product_name = StringField(required= True)
    is_new_product = BooleanField(required = True)
    is_known_product = BooleanField(required = True)
    num_of_wished_surveys = IntField(required = True)
    user_id = ReferenceField('UserAccount')


class ProductPhase(Document):

    is_interview = BooleanField()
    is_derivation = BooleanField()
    is_classification = BooleanField()
    is_final = BooleanField()
    product_id = ReferenceField('Product')



class InterviewPhase(Document):
    
    market = StringField(required = True)
    male = BooleanField()
    female = BooleanField()
    age_range = ListField(required = True)
    description = StringField(required = True)
    product_id = ReferenceField('Product')

class Derivation(Document):
    attributes = ListField(required = True)
    product_id = ReferenceField('Product')

class FinalAttributes(Document):
    final_attributes = ListField(required = True)
    product_id = ReferenceField('Product')

