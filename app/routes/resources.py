"""
SafeLink App - Resources Routes
Handles resource management including shelters, food banks, legal aid, and support services
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.mapbox import MapboxService
from app.routes.auth import token_required
from app.models.shelter import Shelter
from app.models.help_request import HelpRequest
import json

bp = Blueprint('resources', __name__)

@bp.route('/shelters', methods=['GET'])
@token_required
def get_shelters(current_user):
    """Get list of shelters with optional filtering"""
    try:
        # Get query parameters
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', 10, type=float)  # Default 10km radius
        capacity = request.args.get('capacity', type=int)
        services = request.args.getlist('services')  # Multiple services
        gender = request.args.get('gender')
        age_group = request.args.get('age_group')
        
        # Initialize Mapbox service for location-based search
        mapbox = MapboxService()
        
        # Get shelters from database (this would be implemented with actual DB queries)
        shelters = []  # Placeholder - would query actual database
        
        # Filter by location if coordinates provided
        if latitude and longitude:
            shelters = mapbox.filter_by_distance(
                shelters, latitude, longitude, radius
            )
        
        # Filter by other criteria
        if capacity:
            shelters = [s for s in shelters if s.get('available_beds', 0) >= capacity]
        
        if services:
            shelters = [s for s in shelters if any(service in s.get('services', []) for service in services)]
        
        if gender:
            shelters = [s for s in shelters if s.get('gender_restriction') == gender or s.get('gender_restriction') == 'all']
        
        if age_group:
            shelters = [s for s in shelters if age_group in s.get('age_groups', [])]
        
        return jsonify({
            'shelters': shelters,
            'count': len(shelters),
            'filters_applied': {
                'location': bool(latitude and longitude),
                'capacity': capacity,
                'services': services,
                'gender': gender,
                'age_group': age_group
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/food', methods=['GET'])
@token_required
def get_food_resources(current_user):
    """Get list of food banks and meal programs"""
    try:
        # Get query parameters
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', 10, type=float)
        meal_type = request.args.get('meal_type')  # breakfast, lunch, dinner
        days_available = request.args.getlist('days')  # Multiple days
        
        # Get food resources from database
        food_resources = []  # Placeholder - would query actual database
        
        # Filter by location if coordinates provided
        if latitude and longitude:
            mapbox = MapboxService()
            food_resources = mapbox.filter_by_distance(
                food_resources, latitude, longitude, radius
            )
        
        # Filter by meal type
        if meal_type:
            food_resources = [f for f in food_resources if meal_type in f.get('meal_types', [])]
        
        # Filter by days available
        if days_available:
            food_resources = [f for f in food_resources if any(day in f.get('days_available', []) for day in days_available)]
        
        return jsonify({
            'food_resources': food_resources,
            'count': len(food_resources)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/legal', methods=['GET'])
@token_required
def get_legal_aid(current_user):
    """Get list of legal aid services"""
    try:
        # Get query parameters
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', 10, type=float)
        legal_issue = request.args.get('legal_issue')  # housing, immigration, family, etc.
        free_services = request.args.get('free_services', type=bool)
        
        # Get legal aid resources from database
        legal_resources = []  # Placeholder - would query actual database
        
        # Filter by location if coordinates provided
        if latitude and longitude:
            mapbox = MapboxService()
            legal_resources = mapbox.filter_by_distance(
                legal_resources, latitude, longitude, radius
            )
        
        # Filter by legal issue
        if legal_issue:
            legal_resources = [l for l in legal_resources if legal_issue in l.get('specialties', [])]
        
        # Filter by free services
        if free_services:
            legal_resources = [l for l in legal_resources if l.get('free_services', False)]
        
        return jsonify({
            'legal_resources': legal_resources,
            'count': len(legal_resources)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['POST'])
@token_required
def search_resources(current_user):
    """Search for resources by location and criteria"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Search criteria required'}), 400
        
        # Extract search parameters
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = data.get('radius', 10)
        resource_types = data.get('resource_types', [])  # ['shelter', 'food', 'legal', 'medical']
        keywords = data.get('keywords', [])
        urgency_level = data.get('urgency_level', 'medium')
        
        # Initialize Mapbox service
        mapbox = MapboxService()
        
        # Search for resources
        search_results = mapbox.search_resources(
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            resource_types=resource_types,
            keywords=keywords,
            urgency_level=urgency_level
        )
        
        return jsonify({
            'results': search_results['resources'],
            'total_count': search_results['total_count'],
            'search_area': {
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius
            },
            'filters_applied': {
                'resource_types': resource_types,
                'keywords': keywords,
                'urgency_level': urgency_level
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/nearby', methods=['GET'])
@token_required
def get_nearby_resources(current_user):
    """Get all nearby resources based on user location"""
    try:
        # Get user's location from request or profile
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', 5, type=float)  # Default 5km
        
        if not latitude or not longitude:
            return jsonify({'error': 'Location coordinates required'}), 400
        
        # Initialize Mapbox service
        mapbox = MapboxService()
        
        # Get nearby resources
        nearby_resources = mapbox.get_nearby_resources(
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
        
        return jsonify({
            'nearby_resources': nearby_resources,
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<resource_type>/<resource_id>', methods=['GET'])
@token_required
def get_resource_details(current_user, resource_type, resource_id):
    """Get detailed information about a specific resource"""
    try:
        # Validate resource type
        valid_types = ['shelter', 'food', 'legal', 'medical', 'transportation', 'counseling']
        if resource_type not in valid_types:
            return jsonify({'error': 'Invalid resource type'}), 400
        
        # Get resource details from database
        resource_details = {}  # Placeholder - would query actual database
        
        # Add distance if user location provided
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        
        if latitude and longitude and resource_details:
            mapbox = MapboxService()
            distance = mapbox.calculate_distance(
                latitude, longitude,
                resource_details.get('latitude'),
                resource_details.get('longitude')
            )
            resource_details['distance_km'] = distance
        
        return jsonify({
            'resource': resource_details,
            'type': resource_type
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/categories', methods=['GET'])
@token_required
def get_resource_categories(current_user):
    """Get list of available resource categories"""
    try:
        categories = [
            {
                'id': 'shelter',
                'name': 'Emergency Shelters',
                'description': 'Temporary housing and emergency shelters',
                'icon': '🏠'
            },
            {
                'id': 'food',
                'name': 'Food Assistance',
                'description': 'Food banks, meal programs, and nutrition services',
                'icon': '🍽️'
            },
            {
                'id': 'legal',
                'name': 'Legal Aid',
                'description': 'Legal assistance and advocacy services',
                'icon': '⚖️'
            },
            {
                'id': 'medical',
                'name': 'Medical Care',
                'description': 'Healthcare services and medical assistance',
                'icon': '🏥'
            },
            {
                'id': 'transportation',
                'name': 'Transportation',
                'description': 'Transportation assistance and services',
                'icon': '🚗'
            },
            {
                'id': 'counseling',
                'name': 'Counseling & Support',
                'description': 'Mental health and counseling services',
                'icon': '💬'
            }
        ]
        
        return jsonify({
            'categories': categories
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 