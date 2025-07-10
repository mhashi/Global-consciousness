from flask import Blueprint, request, jsonify
from src.models.thought import db, Thought, Story
from datetime import datetime, timedelta
import json
import random

story_generator_bp = Blueprint('story_generator', __name__)

def generate_story_with_ai(thoughts_data):
    """
    Generate a story using AI based on collected thoughts.
    This is a simplified version - in production, you would integrate with
    a proper AI service like OpenAI GPT, Google Gemini, etc.
    """
    
    # Sample story templates based on common themes
    story_templates = {
        'connection': {
            'title': 'Threads of Connection',
            'opening': 'In a world where distance meant nothing and time was just a whisper, {character} discovered that every thought shared was a thread in an invisible tapestry connecting all humanity.',
            'themes': ['unity', 'communication', 'understanding']
        },
        'hope': {
            'title': 'The Light Carriers',
            'opening': 'When the world seemed darkest, {character} found that hope wasn\'t just a feeling—it was a living thing that traveled from heart to heart, growing stronger with each person it touched.',
            'themes': ['optimism', 'resilience', 'future']
        },
        'dreams': {
            'title': 'The Dream Weavers',
            'opening': 'Every night, {character} entered a realm where dreams from around the world converged, creating stories that would inspire the waking world.',
            'themes': ['imagination', 'creativity', 'possibility']
        },
        'change': {
            'title': 'Ripples of Tomorrow',
            'opening': 'The smallest action by {character} created ripples that would eventually reshape the world, proving that change begins with a single thought shared with courage.',
            'themes': ['transformation', 'impact', 'growth']
        }
    }
    
    # Analyze thoughts to determine dominant theme
    all_content = ' '.join([t['content'].lower() for t in thoughts_data])
    
    theme_scores = {}
    for theme, template in story_templates.items():
        score = sum(1 for keyword in template['themes'] if keyword in all_content)
        theme_scores[theme] = score
    
    # Select theme with highest score, or random if tie
    selected_theme = max(theme_scores.keys(), key=lambda k: theme_scores[k])
    if theme_scores[selected_theme] == 0:
        selected_theme = random.choice(list(story_templates.keys()))
    
    template = story_templates[selected_theme]
    
    # Generate character name
    character_names = ['Maya', 'Alex', 'Sam', 'Jordan', 'Riley', 'Casey', 'Morgan', 'Avery']
    character = random.choice(character_names)
    
    # Create story content
    title = template['title']
    opening = template['opening'].format(character=character)
    
    # Build story by incorporating actual thoughts
    story_parts = [opening]
    
    # Select most relevant thoughts
    relevant_thoughts = thoughts_data[:5]  # Take first 5 for simplicity
    
    for i, thought in enumerate(relevant_thoughts):
        if i < 3:  # Incorporate up to 3 thoughts directly
            story_parts.append(f"\n\n{character} remembered the words that had echoed across the digital void: \"{thought['content']}\" These words, shared by someone thousands of miles away, resonated with a truth that transcended borders.")
    
    # Add conclusion
    conclusion = f"\n\nAs {character} reflected on these shared moments of human consciousness, they realized that every thought, every feeling, every dream contributed to a story much larger than any individual life. In this interconnected world, we are all authors of the same magnificent tale."
    
    story_parts.append(conclusion)
    
    full_story = ''.join(story_parts)
    excerpt = full_story[:200] + '...' if len(full_story) > 200 else full_story
    
    return {
        'title': title,
        'content': full_story,
        'excerpt': excerpt
    }

@story_generator_bp.route('/generate-weekly-story', methods=['POST'])
def generate_weekly_story():
    """Generate a new story from recent thoughts"""
    try:
        # Get thoughts from the past week that haven't been used
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        unused_thoughts = Thought.query.filter(
            Thought.created_at >= one_week_ago,
            Thought.used_in_story == False
        ).order_by(Thought.created_at.desc()).all()
        
        if len(unused_thoughts) < 3:
            return jsonify({'error': 'Not enough thoughts to generate a story'}), 400
        
        # Convert to dict format
        thoughts_data = [thought.to_dict() for thought in unused_thoughts]
        
        # Generate story using AI (simplified version)
        story_data = generate_story_with_ai(thoughts_data)
        
        # Create new story in database
        new_story = Story(
            title=story_data['title'],
            content=story_data['content'],
            excerpt=story_data['excerpt'],
            published_at=datetime.utcnow(),
            contributor_count=len(unused_thoughts),
            is_published=True
        )
        
        db.session.add(new_story)
        
        # Mark thoughts as used
        for thought in unused_thoughts:
            thought.used_in_story = True
            thought.story_id = new_story.id
        
        db.session.commit()
        
        return jsonify({
            'message': 'Story generated successfully',
            'story': new_story.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@story_generator_bp.route('/preview-story', methods=['POST'])
def preview_story():
    """Preview what a story would look like without saving it"""
    try:
        # Get recent thoughts for preview
        recent_thoughts = Thought.query.filter(
            Thought.used_in_story == False
        ).order_by(Thought.created_at.desc()).limit(10).all()
        
        if len(recent_thoughts) < 3:
            return jsonify({'error': 'Not enough thoughts for preview'}), 400
        
        thoughts_data = [thought.to_dict() for thought in recent_thoughts]
        story_data = generate_story_with_ai(thoughts_data)
        
        return jsonify({
            'preview': story_data,
            'contributor_count': len(recent_thoughts)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

