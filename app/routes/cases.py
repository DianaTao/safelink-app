"""
SafeLink App - Cases Routes
Handles help request and case management endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.supabase import SupabaseService
from app.routes.auth import token_required
from app.models.case import Case
from datetime import datetime
import json

bp = Blueprint('cases', __name__)

@bp.route('/create', methods=['POST'])
@token_required
def create_case(current_user):
    """Create a new help request/case"""
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('description'):
            return jsonify({'error': 'Title and description are required'}), 400
        
        # Create case object
        case_data = {
            'user_id': current_user['id'],
            'title': data['title'],
            'description': data['description'],
            'category': data.get('category', 'general'),
            'urgency_level': data.get('urgency_level', 'medium'),
            'status': 'open',
            'created_at': datetime.utcnow().isoformat(),
            'location': data.get('location', {}),
            'assigned_to': data.get('assigned_to'),
            'contact_info': data.get('contact_info', {})
        }
        
        # Store case in database (placeholder)
        # case_id = store_case(case_data)
        
        return jsonify({
            'message': 'Case created successfully',
            'case_id': 'temp_id',  # Would be actual case ID from database
            'case_data': case_data
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<case_id>', methods=['GET'])
@token_required
def get_case_details(current_user, case_id):
    """Get details of a specific case"""
    try:
        # Get case details from database
        case_details = {}  # Placeholder - would query actual database
        
        # Validate user permissions
        user_role = current_user.get('role', 'user')
        if user_role == 'user' and case_details.get('user_id') != current_user['id']:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'case': case_details
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<case_id>', methods=['PUT'])
@token_required
def update_case(current_user, case_id):
    """Update a case (status, assignment, notes, etc.)"""
    try:
        data = request.get_json()
        
        # Validate user permissions
        user_role = current_user.get('role', 'user')
        # Only allow update if user is owner or assigned social worker/volunteer
        # Placeholder permission check
        
        # Update case in database (placeholder)
        # update_case(case_id, data)
        
        return jsonify({
            'message': 'Case updated successfully',
            'case_id': case_id,
            'update_data': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/assigned', methods=['GET'])
@token_required
def get_assigned_cases(current_user):
    """Get cases assigned to the current user (for volunteers/social workers)"""
    try:
        user_role = current_user.get('role', 'user')
        if user_role not in ['volunteer', 'social_worker', 'admin']:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Get assigned cases from database
        assigned_cases = []  # Placeholder - would query actual database
        
        return jsonify({
            'assigned_cases': assigned_cases,
            'count': len(assigned_cases)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/my', methods=['GET'])
@token_required
def get_my_cases(current_user):
    """Get cases created by the current user"""
    try:
        # Get cases from database
        my_cases = []  # Placeholder - would query actual database
        
        return jsonify({
            'my_cases': my_cases,
            'count': len(my_cases)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['POST'])
@token_required
def search_cases(current_user):
    """Search for cases by criteria (admin/social worker/volunteer)"""
    try:
        data = request.get_json()
        
        user_role = current_user.get('role', 'user')
        if user_role not in ['admin', 'social_worker', 'volunteer']:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Extract search parameters
        status = data.get('status')
        category = data.get('category')
        assigned_to = data.get('assigned_to')
        urgency_level = data.get('urgency_level')
        created_after = data.get('created_after')
        created_before = data.get('created_before')
        
        # Search cases in database
        search_results = []  # Placeholder - would query actual database
        
        return jsonify({
            'results': search_results,
            'count': len(search_results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 