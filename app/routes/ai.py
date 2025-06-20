"""
SafeLink App - AI Routes
Handles Claude AI integration for intelligent assistance and resource matching
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.claude_api import ClaudeService
from app.routes.auth import token_required
import json

bp = Blueprint('ai', __name__)

@bp.route('/chat', methods=['POST'])
@token_required
def chat(current_user):
    """Chat with Claude AI assistant"""
    try:
        data = request.get_json()
        
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        # Initialize Claude service
        claude = ClaudeService()
        
        # Create context-aware prompt
        context = f"""
        You are a compassionate AI assistant for SafeLink, a platform that helps vulnerable populations 
        find resources and support. The user is: {current_user.get('first_name', 'User')} 
        with role: {current_user.get('role', 'user')}.
        
        Provide helpful, empathetic responses and suggest relevant resources when appropriate.
        """
        
        # Get response from Claude
        response = claude.chat(
            message=data['message'],
            context=context,
            user_id=current_user['id']
        )
        
        return jsonify({
            'response': response['content'],
            'suggestions': response.get('suggestions', []),
            'resources': response.get('resources', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/analyze', methods=['POST'])
@token_required
def analyze_request(current_user):
    """Analyze help request and provide recommendations"""
    try:
        data = request.get_json()
        
        if not data or not data.get('request_text'):
            return jsonify({'error': 'Request text is required'}), 400
        
        # Initialize Claude service
        claude = ClaudeService()
        
        # Analyze the help request
        analysis = claude.analyze_help_request(
            request_text=data['request_text'],
            user_context=current_user,
            urgency_level=data.get('urgency_level', 'medium')
        )
        
        return jsonify({
            'analysis': analysis['analysis'],
            'risk_level': analysis['risk_level'],
            'recommended_resources': analysis['recommended_resources'],
            'priority_score': analysis['priority_score'],
            'suggested_actions': analysis['suggested_actions']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/suggestions', methods=['GET'])
@token_required
def get_suggestions(current_user):
    """Get AI-powered resource suggestions based on user profile"""
    try:
        # Get query parameters
        category = request.args.get('category')
        location = request.args.get('location')
        
        # Initialize Claude service
        claude = ClaudeService()
        
        # Get personalized suggestions
        suggestions = claude.get_resource_suggestions(
            user_profile=current_user,
            category=category,
            location=location
        )
        
        return jsonify({
            'suggestions': suggestions['resources'],
            'reasoning': suggestions['reasoning'],
            'confidence_score': suggestions['confidence_score']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/emergency-assessment', methods=['POST'])
@token_required
def emergency_assessment(current_user):
    """Assess emergency situations and provide immediate guidance"""
    try:
        data = request.get_json()
        
        if not data or not data.get('situation_description'):
            return jsonify({'error': 'Situation description is required'}), 400
        
        # Initialize Claude service
        claude = ClaudeService()
        
        # Assess emergency situation
        assessment = claude.assess_emergency(
            situation=data['situation_description'],
            user_location=data.get('location'),
            user_context=current_user
        )
        
        return jsonify({
            'emergency_level': assessment['emergency_level'],
            'immediate_actions': assessment['immediate_actions'],
            'contact_emergency_services': assessment['contact_emergency_services'],
            'safety_guidance': assessment['safety_guidance'],
            'next_steps': assessment['next_steps']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/case-summary', methods=['POST'])
@token_required
def generate_case_summary(current_user):
    """Generate AI-powered case summary and recommendations"""
    try:
        data = request.get_json()
        
        if not data or not data.get('case_data'):
            return jsonify({'error': 'Case data is required'}), 400
        
        # Initialize Claude service
        claude = ClaudeService()
        
        # Generate case summary
        summary = claude.generate_case_summary(
            case_data=data['case_data'],
            user_role=current_user.get('role'),
            include_recommendations=data.get('include_recommendations', True)
        )
        
        return jsonify({
            'summary': summary['summary'],
            'key_issues': summary['key_issues'],
            'recommendations': summary.get('recommendations', []),
            'risk_factors': summary.get('risk_factors', []),
            'progress_indicators': summary.get('progress_indicators', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/language-translation', methods=['POST'])
@token_required
def translate_message(current_user):
    """Translate messages for multi-language support"""
    try:
        data = request.get_json()
        
        if not data or not data.get('message') or not data.get('target_language'):
            return jsonify({'error': 'Message and target language are required'}), 400
        
        # Initialize Claude service
        claude = ClaudeService()
        
        # Translate message
        translation = claude.translate_message(
            message=data['message'],
            target_language=data['target_language'],
            source_language=data.get('source_language', 'auto')
        )
        
        return jsonify({
            'translated_message': translation['translated_text'],
            'source_language': translation['detected_language'],
            'target_language': data['target_language'],
            'confidence': translation.get('confidence', 0.0)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 