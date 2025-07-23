# server/server/seed_db.py

from app import app, db
from models import User, Room, Booking, Payment, AboutUs
from datetime import datetime, date, timezone

def seed():
    with app.app_context():
        # Recreate database
        db.drop_all()
        db.create_all()

        # Users
        u1 = User(email='test@peirisresort.com', first_name='John', last_name='Doe', phone='+94771234567')
        u1.set_password('12345')
        u2 = User(email='admin@peirisresort.com', first_name='Admin', last_name='User', phone='+94761234568')
        u2.set_password('12345')
        db.session.add_all([u1, u2])
        db.session.commit()

        # Rooms
        rooms_data = [
            ('Ocean View Suite', 'Spacious suite with panoramic ocean views, private balcony, and premium amenities. Perfect for romantic getaways.', 'Suite', 25000.00, 2, 'Ocean View, Private Balcony, King Bed, Mini Bar, Air Conditioning, WiFi, Room Service', 'https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg', True),
            ('Deluxe Beach Room', 'Comfortable room with direct beach access and modern furnishings. Ideal for couples and solo travelers.', 'Deluxe', 18000.00, 2, 'Beach Access, Queen Bed, Air Conditioning, WiFi, Mini Fridge, Coffee Maker', 'https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg', True),
            ('Family Villa', 'Spacious villa perfect for families with separate bedrooms and a private garden area.', 'Villa', 35000.00, 6, 'Private Garden, Two Bedrooms, Living Room, Kitchen, Air Conditioning, WiFi, Parking', 'https://images.pexels.com/photos/1743229/pexels-photo-1743229.jpeg', True),
            ('Standard Twin Room', 'Comfortable twin room with garden view and essential amenities for budget-conscious travelers.', 'Standard', 12000.00, 2, 'Garden View, Twin Beds, Air Conditioning, WiFi, Desk', 'https://images.pexels.com/photos/271643/pexels-photo-271643.jpeg', True),
            ('Presidential Suite', 'Luxurious presidential suite with premium services and unmatched comfort. The ultimate indulgence.', 'Presidential', 50000.00, 4, 'Ocean View, Private Balcony, Jacuzzi, King Bed, Living Room, Butler Service, Mini Bar, Air Conditioning, WiFi', 'https://images.pexels.com/photos/1579253/pexels-photo-1579253.jpeg', True),
            ('Beachfront Bungalow', 'Charming bungalow right on the beach with traditional Sri Lankan architecture and modern comforts.', 'Bungalow', 28000.00, 3, 'Beachfront, Traditional Design, Queen Bed, Air Conditioning, WiFi, Private Entrance', 'https://images.pexels.com/photos/1134176/pexels-photo-1134176.jpeg', True)
        ]
        for name, desc, rtype, price, occ, amenities, url, avail in rooms_data:
            db.session.add(Room(
                name=name,
                description=desc,
                room_type=rtype,
                price_per_night=price,
                max_occupancy=occ,
                amenities=amenities,
                image_url=url,
                is_available=avail
            ))
        db.session.commit()

        # About Us
        about_data = [
            ('About Peiris Grand Resort', 'Peiris Grand Resort Panadura is a premium beachfront destination offering a peaceful escape with a touch of elegance. Located in the scenic coastal town of Panadura, Sri Lanka...', 'main'),
            ('Our Mission', 'To deliver memorable guest experiences through genuine service, comfort, and innovation, while celebrating Sri Lankan hospitality and culture.', 'mission'),
            ('Our Vision', 'To be the leading resort on Sri Lanka\'s western coast, known for excellence in service, sustainable practices, and unforgettable experiences.', 'vision')
        ]
        for title, content, section in about_data:
            db.session.add(AboutUs(title=title, content=content, section=section))
        db.session.commit()

        # Bookings
        booking1 = Booking(user_id=u1.id, room_id=1, check_in_date=date(2024, 2, 15), check_out_date=date(2024, 2, 18), total_amount=75000.00, status='confirmed', special_requests='Late check-in requested')
        booking2 = Booking(user_id=u1.id, room_id=2, check_in_date=date(2024, 3, 1), check_out_date=date(2024, 3, 3), total_amount=36000.00, status='pending', special_requests='Ground floor room preferred')
        db.session.add_all([booking1, booking2])
        db.session.commit()

        # Payments
        payment1 = Payment(booking_id=booking1.id, amount=75000.00, payment_method='Credit Card', transaction_id='TXN123456789', status='completed', processed_at=datetime.now(timezone.utc))
        payment2 = Payment(booking_id=booking2.id, amount=36000.00, payment_method='Bank Transfer', transaction_id='TXN987654321', status='pending', processed_at=None)
        db.session.add_all([payment1, payment2])
        db.session.commit()

    print("Database seeded successfully.")

if __name__ == '__main__':
    seed()
