from flask import Blueprint, request, jsonify
from models.reaction import Reaction
from models.post import Post
from config import db

reaction_bp = Blueprint('reactions', __name__, url_prefix='/api/reactions')


# Add or Update a reaction
@reaction_bp.route('', methods=['POST'])
def add_or_update_reaction():
    """
    Add or update a user's reaction to a post.
    Prevents duplicate reactions per user.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'user_id' not in data or 'post_id' not in data or 'reaction_type' not in data:
            return jsonify({'error': 'Missing required fields: user_id, post_id, reaction_type'}), 400
        
        user_id = data['user_id']
        post_id = data['post_id']
        reaction_type = data['reaction_type']
        
        # Validate reaction_type
        if reaction_type not in ['like', 'dislike']:
            return jsonify({'error': 'reaction_type must be "like" or "dislike"'}), 400
        
        # Check if post exists
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check if user already has a reaction on this post
        existing_reaction = Reaction.query.filter_by(
            user_id=user_id,
            post_id=post_id
        ).first()
        
        if existing_reaction:
            # Update existing reaction
            existing_reaction.reaction_type = reaction_type
            db.session.commit()
            return jsonify({
                'message': 'Reaction updated',
                'reaction': existing_reaction.to_dict()
            }), 200
        else:
            # Create new reaction
            new_reaction = Reaction(
                user_id=user_id,
                post_id=post_id,
                reaction_type=reaction_type
            )
            db.session.add(new_reaction)
            db.session.commit()
            return jsonify({
                'message': 'Reaction added',
                'reaction': new_reaction.to_dict()
            }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get reaction counts for a specific post
@reaction_bp.route('/post/<int:post_id>/counts', methods=['GET'])
def get_reaction_counts(post_id):
    """
    Get the count of likes and dislikes for a specific post.
    """
    try:
        # Check if post exists
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Count likes and dislikes
        likes_count = Reaction.query.filter_by(
            post_id=post_id,
            reaction_type='like'
        ).count()
        
        dislikes_count = Reaction.query.filter_by(
            post_id=post_id,
            reaction_type='dislike'
        ).count()
        
        return jsonify({
            'post_id': post_id,
            'likes': likes_count,
            'dislikes': dislikes_count,
            'total_reactions': likes_count + dislikes_count
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get user's reaction for a specific post
@reaction_bp.route('/post/<int:post_id>/user/<int:user_id>', methods=['GET'])
def get_user_reaction(post_id, user_id):
    """
    Get a specific user's reaction to a post.
    Returns null if user hasn't reacted.
    """
    try:
        reaction = Reaction.query.filter_by(
            user_id=user_id,
            post_id=post_id
        ).first()
        
        if reaction:
            return jsonify({
                'reaction': reaction.to_dict()
            }), 200
        else:
            return jsonify({
                'reaction': None,
                'message': 'User has not reacted to this post'
            }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete a reaction (remove like/dislike)
@reaction_bp.route('/post/<int:post_id>/user/<int:user_id>', methods=['DELETE'])
def delete_reaction(post_id, user_id):
    """
    Remove a user's reaction from a post.
    """
    try:
        reaction = Reaction.query.filter_by(
            user_id=user_id,
            post_id=post_id
        ).first()
        
        if not reaction:
            return jsonify({'error': 'Reaction not found'}), 404
        
        db.session.delete(reaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Reaction removed successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all reactions for a post (optional - for admin/debugging)
@reaction_bp.route('/post/<int:post_id>', methods=['GET'])
def get_all_post_reactions(post_id):
    """
    Get all reactions for a specific post.
    """
    try:
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        reactions = Reaction.query.filter_by(post_id=post_id).all()
        
        return jsonify({
            'post_id': post_id,
            'reactions': [reaction.to_dict() for reaction in reactions]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500