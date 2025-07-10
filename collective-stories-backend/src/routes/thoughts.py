from flask import Blueprint, request, jsonify
from src.models.thought import db, Thought, Story
from datetime import datetime, timedelta
import requests
import json

thoughts_bp = Blueprint('thoughts', __name__)

def get_location_from_ip(ip_address):
    """Get location from IP address using a free geolocation service"""
    try:
        # Using ipapi.co for free IP geolocation
        response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            city = data.get('city', 'Unknown')
            country = data.get('country_name', 'Unknown')
            return f"{city}, {country}"
    except:
        pass
    return "Unknown Location"

@thoughts_bp.route('/thoughts', methods=['POST'])
def submit_thought():
    """Submit a new thought"""
    try:
        data = request.get_json()
        
        if not data or not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        content = data.get('content', '').strip()
        if len(content) > 500:
            return jsonify({'error': 'Content must be 500 characters or less'}), 400
        
        # Get client IP
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        # Get location from IP
        location = get_location_from_ip(ip_address) if ip_address != '127.0.0.1' else "Local Development"
        
        # Create new thought
        thought = Thought(
            content=content,
            tags=','.join(data.get('tags', [])) if data.get('tags') else None,
            is_anonymous=data.get('is_anonymous', True),
            location=location,
            ip_address=ip_address
        )
        
        db.session.add(thought)
        db.session.commit()
        
        return jsonify({
            'message': 'Thought submitted successfully',
            'thought': thought.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@thoughts_bp.route('/thoughts/recent', methods=['GET'])
def get_recent_thoughts():
    """Get recent thoughts for display"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        thoughts = Thought.query.order_by(Thought.created_at.desc()).limit(limit).all()
        
        # Format for display (anonymize content if needed)
        recent_thoughts = []
        for thought in thoughts:
            thought_data = thought.to_dict()
            # Truncate content for preview
            if len(thought_data['content']) > 100:
                thought_data['content'] = thought_data['content'][:97] + '...'
            recent_thoughts.append(thought_data)
        
        return jsonify(recent_thoughts), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@thoughts_bp.route('/stories/current', methods=['GET'])
def get_current_story():
    """Get the current week's story"""
    try:
        # Get the most recent published story
        current_story = Story.query.filter_by(is_published=True).order_by(Story.published_at.desc()).first()
        
        if not current_story:
            # Return a default story if none exists
            return jsonify({
                'title': 'Echoes of Tomorrow',
                'excerpt': 'In a world where thoughts traveled faster than light, Maria discovered that her morning coffee ritual connected her to a baker in Tokyo, a student in São Paulo, and a grandmother in Cairo...',
                'published_at': datetime.utcnow().isoformat(),
                'contributor_count': 847
            }), 200
        
        return jsonify(current_story.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@thoughts_bp.route('/stories', methods=['GET'])
def get_stories():
    """Get all published stories"""
    try:
        stories = Story.query.filter_by(is_published=True).order_by(Story.published_at.desc()).all()
        
        # If no stories exist, return sample data
        if not stories:
            sample_stories = [
                {
                    'title': 'The Language of Silence',
                    'published_at': (datetime.utcnow() - timedelta(days=7)).isoformat(),
                    'contributor_count': 923
                },
                {
                    'title': 'Bridges Made of Light',
                    'published_at': (datetime.utcnow() - timedelta(days=14)).isoformat(),
                    'contributor_count': 756
                },
                {
                    'title': 'The Collector of Moments',
                    'published_at': (datetime.utcnow() - timedelta(days=21)).isoformat(),
                    'contributor_count': 834
                },
                {
                    'title': 'When Time Stood Still',
                    'published_at': (datetime.utcnow() - timedelta(days=28)).isoformat(),
                    'contributor_count': 692
                }
            ]
            return jsonify(sample_stories), 200
        
        return jsonify([story.to_dict() for story in stories]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@thoughts_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    try:
        total_thoughts = Thought.query.count()
        total_stories = Story.query.filter_by(is_published=True).count()
        
        # Count unique locations (approximate countries)
        unique_locations = db.session.query(Thought.location).distinct().count()
        
        return jsonify({
            'total_thoughts': total_thoughts or 12847,  # Default values for demo
            'total_stories': total_stories or 52,
            'countries_represented': unique_locations or 127
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

