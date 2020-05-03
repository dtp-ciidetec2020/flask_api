from flask import Blueprint
from flask import request
from flask import jsonify


from app.Models.product_schema import Product 
from app.Models.user_schema import UserAccount


from flask_jwt_extended import ( jwt_required, create_access_token, get_jwt_identity)


product_creation_flow = Blueprint('product_creation_flow', __name__)


@product_creation_flow.route('/product-creation', methods=['POST'])
@jwt_required
def create_product():
    #Validar un solo producto con el mismo nombre para el mismo usuario
    status = None

    docUserObj = UserAccount.objects(username = get_jwt_identity() )
    if_product_name = Product.objects(user_id = docUserObj, 
                        product_name =  request.json.get('product_name', None) )

    if if_product_name is not None:
        status = "product already exist please verify"
    else:
        new_product = Product(
            product_name = request.json.get('product_name', None),
            is_new_product = request.json.get('is_new_product', None),
            is_known_product = request.json.get('is_kwon_product', None),
            num_of_wished_surveys = request.json.get('num_of_wished_surveys', None),
            user_id = request.json.get(docUserObj, None)
        )
        try:
            new_product.save()
            status = "created",201
        except:
            status = "not created"
        
    return jsonify(status=status)


@product_creation_flow.route('/production-creation/status', methods=['GET'])
def create_product_status():

    username = get_jwt_identity()
    docUserObj = UserAccount.objects(username = username)
    docProdObj = Product.objects(user_id = docUserObj )

@product_creation_flow.route('/product-creation/interview-phase', methods=['POST'])
def create_product_interview():
    pass