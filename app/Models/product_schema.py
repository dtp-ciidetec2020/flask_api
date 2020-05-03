from mongoengine import *
from flask import jsonify


class Product(Document):

    product_name = StringField()
    is_new_product = BooleanField()
    is_known_product = BooleanField()
    num_of_wished_surveys = IntField()
    user_id = ReferenceField('UserAccount')


class ProductPhase(Document):

    """
    Esta coleccion se  tiene que crear cuando un producto es creado
    """
    
    is_interview_done = BooleanField(default=False)
    is_derivation_done = BooleanField(default=False)
    is_classification_done = BooleanField(default=False)
    is_final_done = BooleanField(default=False)
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

