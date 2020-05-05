from flask import Blueprint
from flask import request
from flask import jsonify


from bson.json_util import dumps, loads

from app.Models.product_schema import (
    Product, ProductPhaseStatus, InterviewPhase,AttributesDerivation, FinalAttributes
)

from app.Models.user_schema import UserAccount


from flask_jwt_extended import ( jwt_required, create_access_token, get_jwt_identity)


product_creation_flow = Blueprint('product_creation_flow', __name__)



@product_creation_flow.route('/profile/<username>/products', methods=['GET'])
@jwt_required
def user_products(username):
    
    status = None
    
    list_of_products= map(lambda product: product, Product.objects(user_id= loads(get_jwt_identity()['id'])) )
    list_of_products = list(list_of_products)
    if not list_of_products:
        status = "There are not products avalibele"
    else:
        status = list_of_products

    return jsonify(status=status), 200

@product_creation_flow.route('/product-creation', methods=['POST'])
@jwt_required
def create_product():
    #Validar un solo producto con el mismo nombre para el mismo usuario
    status = None

    if_product_name = map(lambda product: product.product_name, Product.objects(user_id =loads(get_jwt_identity()['id'] ), product_name=request.json.get('product_name') ) )
    
    if list(if_product_name)    :
        status = "product already exist please verify"
    else:
        new_product = Product(
            product_name = request.json.get('product_name', None),
            is_new_product = request.json.get('is_new_product', None),
            is_known_product = request.json.get('is_kwon_product', None),
            num_of_wished_surveys = request.json.get('num_of_wished_surveys', None),
            user_id =  loads(get_jwt_identity()['id'])
        )
        try:
            new_product.save()
            try:
                ProductPhaseStatus(product_id = new_product.id).save()
            except:
                status = "something odd just happened"
            status = "created",201
        except:
            status = "not created"

    return jsonify(status=status)


@product_creation_flow.route('/product-creation/<product_id>/status', methods=['GET'])
@jwt_required
def create_product_status(product_id):

    status = None

    product_phases_status = ProductPhaseStatus.objects(product_id =  product_id)

    return jsonify(status=product_phases_status)

@product_creation_flow.route('/product-creation/<product_id>/interview-phase', methods=['POST'])
@jwt_required
def create_product_interview(product_id):
    
    status = None

    interview_phase_obj = InterviewPhase(
        market = request.json.get('market',None),
        male = request.json.get('male', None),
        female = request.json.get('female',None),
        age_range = request.json.get('age_range',None),
        description = request.json.get('description', None),
        product_id = product_id
    )
    try:
        interview_phase_obj.save()
        status = "created"
        try:
            product_phases_status = ProductPhaseStatus.objects(product_id = product_id )
            product_phases_status.update(is_interview_done = True)
        except:
            status = "error"
    except:
        status ="something went wrong"

    return jsonify(status=status),200

@product_creation_flow.route('/product-creation/<product_id>/attributes-derivation',methods=['POST'])
@jwt_required
def create_product_attributes_derivation(product_id):
    status = None
    attributes_list = AttributesDerivation(attributes=request.json.get('attributes',None), product_id = product_id)
    try:
        attributes_list.save()
        status = "created",201
        try:
            product_phases_status = ProductPhaseStatus.objects(product_id = product_id)
            product_phases_status.update(is_derivation_done = True)
        except:
            status = "error"
    except:
        status="error"
    
    return jsonify(status=status)

@product_creation_flow.route('/product-creation/<product_id>/show-attributes', methods=['GET'])
@jwt_required
def create_product_show_attributes(product_id):

    attributes_list = AttributesDerivation.objects(product_id = product_id)
    
    return jsonify(attributes=attributes_list)

@product_creation_flow.route('/product-creation/<product_id>/post-to-final', methods=['POST'])
@jwt_required
def create_product_final_attributes(product_id):

    status = None
    
    fattributes = FinalAttributes(final_attributes = request.json.get('attributes',None), product_id= product_id)
    
    try:
        fattributes.save()
        status = "created",201
        try:
            product_phases_status =  ProductPhaseStatus.objects(product_id = product_id)
            product_phases_status.update(is_classification_done = True, is_final_done = True)
        except:
            status = "something went wrong"
    except:
        status = "product already exist"
    return jsonify(status=status)

@product_creation_flow.route('/product-creation/<product_id>/show-final-attributes',methods=['GET'])
@jwt_required
def create_product_show_final_attributes(product_id):
    status = None
    fattributes = FinalAttributes.objects(product_id = product_id)
    
    return jsonify(attributes = fattributes),200

"""
Delete some collections if change opinion?
"""
