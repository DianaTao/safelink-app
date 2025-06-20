"""
SafeLink App - Alerts Routes
Handles emergency notification system and alert management
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.sms import SMSService
from app.routes.auth import token_required
from app.models.case import Case
from datetime import datetime, timedelta
import json

bp = Blueprint('alerts', __name__)

@bp.route('/emergency', methods=['POST'])
@token_required
def send_emergency_alert(current_user):
    """Send emergency alert to appropriate responders"""
    try:
        data = request.get_json()
        
        if not data or not data.get('emergency_type') or not data.get('description'):
            return jsonify({'error': 'Emergency type and description are required'}), 400
        
        # Extract alert data
        emergency_type = data['emergency_type']
        description = data['description']
        location = data.get('location', {})
        urgency_level = data.get('urgency_level', 'high')
        contact_info = data.get('contact_info', {})
        
        # Create alert record
        alert_data = {
            'user_id': current_user['id'],
            'emergency_type': emergency_type,
            'description': description,
            'location': location,
            'urgency_level': urgency_level,
            'contact_info': contact_info,
            'status': 'active',
            'created_at': datetime.utcnow().isoformat(),
            'responders_notified': []
        }
        
        # Initialize SMS service
        sms = SMSService()
        
        # Determine appropriate responders based on emergency type
        responders = get_responders_for_emergency(emergency_type, location)
        
        # Send SMS notifications to responders
        notifications_sent = []
        for responder in responders:
            try:
                message = create_emergency_message(alert_data, responder)
                sms_result = sms.send_message(
                    to=responder['phone'],
                    message=message,
                    priority='high'
                )
                
                if sms_result['success']:
                    notifications_sent.append({
                        'responder_id': responder['id'],
                        'phone': responder['phone'],
                        'sent_at': datetime.utcnow().isoformat()
                    })
                    
            except Exception as e:
                current_app.logger.error(f"Failed to send SMS to {responder['phone']}: {str(e)}")
        
        # Update alert with notification results
        alert_data['responders_notified'] = notifications_sent
        alert_data['notifications_sent'] = len(notifications_sent)
        
        # Store alert in database (placeholder)
        # alert_id = store_alert(alert_data)
        
        return jsonify({
            'message': 'Emergency alert sent successfully',
            'alert_id': 'temp_id',  # Would be actual alert ID from database
            'notifications_sent': len(notifications_sent),
            'responders_contacted': len(responders),
            'alert_data': alert_data
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/active', methods=['GET'])
@token_required
def get_active_alerts(current_user):
    """Get active emergency alerts"""
    try:
        # Get query parameters
        user_role = current_user.get('role', 'user')
        location = request.args.get('location')  # Optional location filter
        emergency_type = request.args.get('emergency_type')
        
        # Get active alerts from database
        active_alerts = []  # Placeholder - would query actual database
        
        # Filter alerts based on user role and permissions
        if user_role == 'user':
            # Users can only see their own alerts
            active_alerts = [alert for alert in active_alerts if alert['user_id'] == current_user['id']]
        elif user_role in ['volunteer', 'social_worker']:
            # Volunteers and social workers can see alerts in their area
            if location:
                active_alerts = filter_alerts_by_location(active_alerts, location)
        
        # Filter by emergency type if specified
        if emergency_type:
            active_alerts = [alert for alert in active_alerts if alert['emergency_type'] == emergency_type]
        
        return jsonify({
            'active_alerts': active_alerts,
            'count': len(active_alerts),
            'user_role': user_role
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<alert_id>/resolve', methods=['PUT'])
@token_required
def resolve_alert(current_user, alert_id):
    """Resolve an emergency alert"""
    try:
        data = request.get_json()
        
        # Validate user permissions
        user_role = current_user.get('role', 'user')
        if user_role == 'user':
            # Users can only resolve their own alerts
            # Check if alert belongs to user
            pass
        
        # Update alert status
        resolution_data = {
            'status': 'resolved',
            'resolved_by': current_user['id'],
            'resolved_at': datetime.utcnow().isoformat(),
            'resolution_notes': data.get('resolution_notes', ''),
            'resolution_method': data.get('resolution_method', '')
        }
        
        # Update alert in database (placeholder)
        # update_alert(alert_id, resolution_data)
        
        # Send resolution notification if needed
        if data.get('notify_user', False):
            sms = SMSService()
            user_phone = current_user.get('phone')
            if user_phone:
                resolution_message = f"Your emergency alert has been resolved. Resolution: {resolution_data['resolution_notes']}"
                sms.send_message(to=user_phone, message=resolution_message)
        
        return jsonify({
            'message': 'Alert resolved successfully',
            'alert_id': alert_id,
            'resolution_data': resolution_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<alert_id>', methods=['GET'])
@token_required
def get_alert_details(current_user, alert_id):
    """Get detailed information about a specific alert"""
    try:
        # Get alert details from database
        alert_details = {}  # Placeholder - would query actual database
        
        # Validate user permissions
        user_role = current_user.get('role', 'user')
        if user_role == 'user' and alert_details.get('user_id') != current_user['id']:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'alert': alert_details
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/respond', methods=['POST'])
@token_required
def respond_to_alert(current_user):
    """Respond to an emergency alert (for volunteers/social workers)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('alert_id'):
            return jsonify({'error': 'Alert ID is required'}), 400
        
        # Validate user role
        user_role = current_user.get('role', 'user')
        if user_role not in ['volunteer', 'social_worker', 'admin']:
            return jsonify({'error': 'Insufficient permissions to respond to alerts'}), 403
        
        alert_id = data['alert_id']
        response_data = {
            'responder_id': current_user['id'],
            'responder_name': f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}",
            'response_time': datetime.utcnow().isoformat(),
            'response_type': data.get('response_type', 'acknowledged'),
            'estimated_arrival': data.get('estimated_arrival'),
            'notes': data.get('notes', '')
        }
        
        # Update alert with response (placeholder)
        # update_alert_response(alert_id, response_data)
        
        # Notify alert creator about response
        sms = SMSService()
        # Get alert creator's phone number and send notification
        
        return jsonify({
            'message': 'Response recorded successfully',
            'alert_id': alert_id,
            'response_data': response_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/test', methods=['POST'])
@token_required
def test_alert_system(current_user):
    """Test the alert system (for development/testing)"""
    try:
        data = request.get_json()
        
        # Only allow in development/testing environment
        if current_app.config['ENV'] == 'production':
            return jsonify({'error': 'Test endpoint not available in production'}), 403
        
        # Send test alert
        test_alert_data = {
            'emergency_type': 'test',
            'description': 'This is a test emergency alert',
            'urgency_level': 'low',
            'contact_info': current_user.get('phone', '')
        }
        
        # Process test alert
        result = send_emergency_alert(current_user)
        
        return jsonify({
            'message': 'Test alert sent successfully',
            'test_data': test_alert_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_responders_for_emergency(emergency_type, location):
    """Get appropriate responders for emergency type and location"""
    # This would query the database for available responders
    # Placeholder implementation
    responders = []
    
    # Example responder mapping
    emergency_responder_map = {
        'medical': ['paramedics', 'doctors', 'nurses'],
        'fire': ['firefighters', 'emergency_services'],
        'police': ['police_officers', 'security'],
        'domestic_violence': ['social_workers', 'counselors', 'police_officers'],
        'homelessness': ['social_workers', 'shelter_staff'],
        'mental_health': ['counselors', 'psychiatrists', 'social_workers']
    }
    
    required_roles = emergency_responder_map.get(emergency_type, ['emergency_responders'])
    
    # Query database for responders with required roles in location
    # responders = query_responders(required_roles, location)
    
    return responders

def create_emergency_message(alert_data, responder):
    """Create emergency message for responder"""
    message = f"""
EMERGENCY ALERT - SafeLink

Type: {alert_data['emergency_type'].upper()}
Urgency: {alert_data['urgency_level'].upper()}
Description: {alert_data['description']}

Location: {alert_data.get('location', {}).get('address', 'N/A')}
Contact: {alert_data.get('contact_info', {}).get('phone', 'N/A')}

Please respond immediately if available.
    """.strip()
    
    return message

def filter_alerts_by_location(alerts, location):
    """Filter alerts by location"""
    # Implement location-based filtering logic
    return alerts 