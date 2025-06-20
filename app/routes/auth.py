"""
SafeLink App - Authentication Routes
Handles user registration, login, logout, and profile management with Supabase
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.supabase import SupabaseService
from app.models.user import User
from functools import wraps
import jwt
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Verify token with Supabase
            supabase = SupabaseService()
            user_data = supabase.verify_token(token)
            current_user = user_data
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Register user with Supabase
        supabase = SupabaseService()
        user_data = supabase.register_user(
            email=data['email'],
            password=data['password'],
            user_metadata={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data.get('phone'),
                'role': data.get('role', 'user')
            }
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user_data
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate with Supabase
        supabase = SupabaseService()
        auth_data = supabase.login_user(data['email'], data['password'])
        
        return jsonify({
            'message': 'Login successful',
            'access_token': auth_data['access_token'],
            'refresh_token': auth_data['refresh_token'],
            'user': auth_data['user']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """User logout endpoint"""
    try:
        # Logout from Supabase
        supabase = SupabaseService()
        supabase.logout_user()
        
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get user profile"""
    try:
        return jsonify({
            'user': current_user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile"""
    try:
        data = request.get_json()
        
        # Update user profile in Supabase
        supabase = SupabaseService()
        updated_user = supabase.update_user_profile(current_user['id'], data)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': updated_user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('refresh_token'):
            return jsonify({'error': 'Refresh token is required'}), 400
        
        # Refresh token with Supabase
        supabase = SupabaseService()
        auth_data = supabase.refresh_token(data['refresh_token'])
        
        return jsonify({
            'access_token': auth_data['access_token'],
            'refresh_token': auth_data['refresh_token']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401 