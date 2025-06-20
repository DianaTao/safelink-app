"""
SafeLink App - Users Routes
Handles user profile management, volunteer and social worker roles
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.supabase import SupabaseService
from app.routes.auth import token_required
from app.models.user import User
from datetime import datetime
import json

bp = Blueprint('users', __name__)

@bp.route('/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    """Get current user's profile"""
    try:
        # Get detailed profile from database
        profile = {}  # Placeholder - would query actual database
        
        return jsonify({
            'profile': profile or current_user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    """Update current user's profile"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Profile data is required'}), 400
        
        # Validate updateable fields
        allowed_fields = [
            'first_name', 'last_name', 'phone', 'address', 'emergency_contact',
            'preferences', 'languages', 'accessibility_needs', 'volunteer_interests'
        ]
        
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        # Update profile in database
        supabase = SupabaseService()
        updated_profile = supabase.update_user_profile(current_user['id'], update_data)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': updated_profile
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/volunteers', methods=['GET'])
@token_required
def get_volunteers(current_user):
    """Get list of volunteers (for authorized users)"""
    try:
        # Check user permissions
        user_role = current_user.get('role', 'user')
        if user_role not in ['admin', 'social_worker', 'coordinator']:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Get query parameters
        location = request.args.get('location')
        skills = request.args.getlist('skills')
        availability = request.args.get('availability')
        status = request.args.get('status', 'active')
        
        # Get volunteers from database
        volunteers = []  # Placeholder - would query actual database
        
        # Apply filters
        if location:
            volunteers = filter_volunteers_by_location(volunteers, location)
        
        if skills:
            volunteers = [v for v in volunteers if any(skill in v.get('skills', []) for skill in skills)]
        
        if availability:
            volunteers = [v for v in volunteers if availability in v.get('availability', [])]
        
        if status:
            volunteers = [v for v in volunteers if v.get('status') == status]
        
        return jsonify({
            'volunteers': volunteers,
            'count': len(volunteers),
            'filters_applied': {
                'location': location,
                'skills': skills,
                'availability': availability,
                'status': status
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/social-workers', methods=['GET'])
@token_required
def get_social_workers(current_user):
    """Get list of social workers (for authorized users)"""
    try:
        # Check user permissions
        user_role = current_user.get('role', 'user')
        if user_role not in ['admin', 'coordinator']:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Get query parameters
        location = request.args.get('location')
        specialties = request.args.getlist('specialties')
        availability = request.args.get('availability')
        
        # Get social workers from database
        social_workers = []  # Placeholder - would query actual database
        
        # Apply filters
        if location:
            social_workers = filter_users_by_location(social_workers, location)
        
        if specialties:
            social_workers = [sw for sw in social_workers if any(spec in sw.get('specialties', []) for spec in specialties)]
        
        if availability:
            social_workers = [sw for sw in social_workers if availability in sw.get('availability', [])]
        
        return jsonify({
            'social_workers': social_workers,
            'count': len(social_workers)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/volunteer/register', methods=['POST'])
@token_required
def register_volunteer(current_user):
    """Register current user as a volunteer"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Volunteer information is required'}), 400
        
        # Validate required fields
        required_fields = ['skills', 'availability', 'emergency_contact']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create volunteer profile
        volunteer_data = {
            'user_id': current_user['id'],
            'skills': data['skills'],
            'availability': data['availability'],
            'emergency_contact': data['emergency_contact'],
            'background_check': data.get('background_check', False),
            'training_completed': data.get('training_completed', []),
            'preferences': data.get('preferences', {}),
            'status': 'pending_approval',
            'registered_at': datetime.utcnow().isoformat()
        }
        
        # Store volunteer registration in database
        # volunteer_id = store_volunteer_registration(volunteer_data)
        
        # Update user role
        supabase = SupabaseService()
        supabase.update_user_profile(current_user['id'], {'role': 'volunteer_pending'})
        
        return jsonify({
            'message': 'Volunteer registration submitted successfully',
            'volunteer_data': volunteer_data,
            'status': 'pending_approval'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/volunteer/approve/<user_id>', methods=['PUT'])
@token_required
def approve_volunteer(current_user, user_id):
    """Approve volunteer registration (admin/social worker only)"""
    try:
        # Check user permissions
        user_role = current_user.get('role', 'user')
        if user_role not in ['admin', 'social_worker', 'coordinator']:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        # Update volunteer status
        approval_data = {
            'status': 'approved',
            'approved_by': current_user['id'],
            'approved_at': datetime.utcnow().isoformat(),
            'notes': data.get('notes', '')
        }
        
        # Update volunteer status in database
        # update_volunteer_status(user_id, approval_data)
        
        # Update user role
        supabase = SupabaseService()
        supabase.update_user_profile(user_id, {'role': 'volunteer'})
        
        return jsonify({
            'message': 'Volunteer approved successfully',
            'user_id': user_id,
            'approval_data': approval_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/volunteer/<user_id>', methods=['GET'])
@token_required
def get_volunteer_details(current_user, user_id):
    """Get detailed volunteer information"""
    try:
        # Check user permissions
        user_role = current_user.get('role', 'user')
        if user_role == 'user' and current_user['id'] != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get volunteer details from database
        volunteer_details = {}  # Placeholder - would query actual database
        
        return jsonify({
            'volunteer': volunteer_details
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/availability', methods=['PUT'])
@token_required
def update_availability(current_user):
    """Update user availability (for volunteers/social workers)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('availability'):
            return jsonify({'error': 'Availability information is required'}), 400
        
        # Validate user role
        user_role = current_user.get('role', 'user')
        if user_role not in ['volunteer', 'social_worker']:
            return jsonify({'error': 'Only volunteers and social workers can update availability'}), 403
        
        # Update availability in database
        availability_data = {
            'availability': data['availability'],
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # update_user_availability(current_user['id'], availability_data)
        
        return jsonify({
            'message': 'Availability updated successfully',
            'availability': data['availability']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/preferences', methods=['PUT'])
@token_required
def update_preferences(current_user):
    """Update user preferences"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Preferences data is required'}), 400
        
        # Update preferences in database
        preferences_data = {
            'preferences': data,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # update_user_preferences(current_user['id'], preferences_data)
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/stats', methods=['GET'])
@token_required
def get_user_stats(current_user):
    """Get user statistics and activity summary"""
    try:
        # Get user statistics from database
        stats = {
            'total_cases': 0,  # Placeholder
            'active_cases': 0,  # Placeholder
            'completed_cases': 0,  # Placeholder
            'volunteer_hours': 0,  # Placeholder
            'alerts_sent': 0,  # Placeholder
            'resources_accessed': 0,  # Placeholder
            'last_activity': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'stats': stats,
            'user_id': current_user['id']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def filter_volunteers_by_location(volunteers, location):
    """Filter volunteers by location"""
    # Implement location-based filtering logic
    return volunteers

def filter_users_by_location(users, location):
    """Filter users by location"""
    # Implement location-based filtering logic
    return users 