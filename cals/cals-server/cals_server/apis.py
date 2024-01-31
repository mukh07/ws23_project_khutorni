from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields, reqparse

from cals_sdk.cvat import CVATApiClient, CVATClient
from cals_sdk.projects import Projects


# Create the Flask blueprint and add the API
api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    api_blueprint,
    title='CALS API',
    version='1.0',
    description='REST API for Continuial Active Learning System (CALS)',
    doc='/doc'
)

# Create the Flask namespaces
dataset_ns = Namespace('datasets', description='Datasets')

# Add the Flask namespaces to the API
api.add_namespace(dataset_ns)

# Create the Flask models
dataset_model = api.model('Dataset', {
    'id': fields.String(required=True, description='The dataset unique identifier'),
    'name': fields.String(required=True, description='The dataset name'),
    'description': fields.String(required=True, description='The dataset description'),
    'num_keypoints': fields.Integer(required=True, description='The number of keypoints'),
    'skeleton_svg': fields.String(required=True, description='The skeleton SVG'),
    'url': fields.Url('dataset', absolute=True, scheme='https')
})


# # Create a request parser for POST
# login_reqparser = reqparse.RequestParser()
# login_reqparser.add_argument('username', type=str, required=True, help='The username')
# login_reqparser.add_argument('password', type=str, required=True, help='The password')


# Create the Flask resources
@dataset_ns.route('')
class DatasetList(Resource):
    @dataset_ns.doc('list_datasets')
    def get(self):
        """ List all datasets """
        return [
            {
                'id': 'coco',
                'name': 'COCO',
                'description': 'COCO Keypoints Challenge 2017',
                'num_keypoints': 17,
                'skeleton_svg': 'https://raw.githubusercontent.com/leVirve/COCO-KeypointsChallenge/master/data/skeleton.svg',
                'url': 'https://cocodataset.org/#keypoints-2017'
            }
        ]

    # @dataset_ns.doc('create_dataset')
    # @dataset_ns.expect(login_reqparser)
    # def post(self):
    #     """ Create a new dataset """
    #     args = login_reqparser.parse_args()
    #     username = args['username']
    #     password = args['password']

    # def put(self):
    #     """ Update a dataset """
    #     pass


# Create a CVAT namespace
cvat_ns = Namespace('cvat', description='CVAT')

# Add the CVAT namespace to the API
api.add_namespace(cvat_ns)


# cvat args parser
cvat_parser = cvat_ns.parser()
cvat_parser.add_argument('username', type=str,
                         help='CVAT username', required=True)
cvat_parser.add_argument('password', type=str,
                         help='CVAT password', required=True)


@cvat_ns.route('/auth/login')
class CVATLogin(Resource):
    @cvat_ns.doc('auth')
    @cvat_ns.expect(cvat_parser)
    def post(self):
        """ Authenticate with CVAT """
        args = cvat_parser.parse_args()
        username = args['username']
        password = args['password']

        client = CVATApiClient.get_instance()
        status = client.authenticate(username, password)
        return {
            'status': status,
            'token': client.auth_token,
        }


@cvat_ns.route('/auth/logout')
class CVATLogin(Resource):
    @cvat_ns.doc('auth')
    def post(self):
        """ Authenticate with CVAT """
        client = CVATApiClient.get_instance()
        client.clear_auth_token()
        return {'status': True}


@cvat_ns.route('/auth/token')
class CVATAuthToken(Resource):
    @cvat_ns.doc('auth')
    def get(self):
        """ Get CVAT auth token """
        client = CVATApiClient.get_instance()
        return {'token': client.auth_token}


@cvat_ns.route('/projects')
class CVATProjects(Resource):
    @cvat_ns.doc('projects')
    def get(self):
        """ List CVAT projects """
        client = CVATClient.get_instance()
        try:
            projects = client.get_projects()
        # except FileNotFoundError:
        #     return {'error': 'Project does not exist'}, 404
        except ValueError:
            return {'error': 'No credentials set'}, 401

        return projects

