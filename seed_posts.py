#!/usr/bin/env python3
"""
Simple script to seed sample posts for Campus Pulse+
"""

from app import create_app, db
from models.post import Post

def seed_posts():
    """Create sample posts for testing"""

    # Sample post data
    sample_posts = [
        {
            "content": "The cafeteria food quality has really improved this semester! The new menu options are much better and more variety. Keep up the good work kitchen staff! 🍽️",
            "image": "https://picsum.photos/600/400?random=1",
            "user_id": 1,
            "category_id": 1
        },
        {
            "content": "WiFi in the library is extremely slow during peak hours. Students can't focus on assignments because pages take forever to load. This needs urgent attention! 📚💻",
            "image": "https://picsum.photos/600/400?random=2",
            "user_id": 1,
            "category_id": 1
        },
        {
            "content": "The new sports complex is amazing! The facilities are top-notch and perfect for staying fit during studies. Love the basketball courts and gym equipment. 🏀💪",
            "image": "https://picsum.photos/600/400?random=3",
            "user_id": 1,
            "category_id": 1
        },
        {
            "content": "Parking situation on campus is getting worse. With more students, we need more parking spaces or better shuttle services. It's frustrating to circle for 30 minutes looking for a spot. 🚗😩",
            "image": "https://picsum.photos/600/400?random=4",
            "user_id": 1,
            "category_id": 1
        }
    ]

    app = create_app('development')

    with app.app_context():
        # Clear existing posts (optional)
        Post.query.delete()
        db.session.commit()

        # Create sample posts
        for post_data in sample_posts:
            post = Post(
                content=post_data["content"],
                image=post_data["image"],
                user_id=post_data["user_id"],
                category_id=post_data["category_id"]
            )
            db.session.add(post)

        db.session.commit()
        print("✅ Successfully seeded 4 sample posts!")

if __name__ == "__main__":
    seed_posts()