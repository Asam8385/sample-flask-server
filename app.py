from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime, date
from config import Config
from models import db, User, Room, Booking, Payment, AboutUs

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions this is backend and need to run to connect this with mysql database
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Create tables
with app.app_context():
    db.create_all()

# Authentication Routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Room Routes
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    try:
        rooms = Room.query.filter_by(is_available=True).all()
        return jsonify([room.to_dict() for room in rooms]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    try:
        room = Room.query.get_or_404(room_id)
        return jsonify(room.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Booking Routes
@app.route('/api/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Parse dates
        check_in = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
        check_out = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
        
        # Calculate total amount
        room = Room.query.get(data['room_id'])
        if not room:
            return jsonify({'error': 'Room not found'}), 404
            
        days = (check_out - check_in).days
        total_amount = float(room.price_per_night) * days
        
        # Create booking
        booking = Booking(
            user_id=user_id,
            room_id=data['room_id'],
            check_in_date=check_in,
            check_out_date=check_out,
            total_amount=total_amount,
            special_requests=data.get('special_requests')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_bookings(user_id):
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        bookings = Booking.query.filter_by(user_id=user_id).all()
        return jsonify([booking.to_dict() for booking in bookings]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Profile Routes
@app.route('/api/profile/<int:user_id>', methods=['GET'])
@jwt_required()
def get_profile(user_id):
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payment Routes
@app.route('/api/payments', methods=['POST'])
@jwt_required()
def process_payment():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Verify booking belongs to user
        booking = Booking.query.get(data['booking_id'])
        if not booking or booking.user_id != user_id:
            return jsonify({'error': 'Booking not found or unauthorized'}), 404
            
        # Create payment record
        payment = Payment(
            booking_id=data['booking_id'],
            amount=data['amount'],
            payment_method=data['payment_method'],
            transaction_id=data.get('transaction_id'),
            status='completed',  # Demo - always successful
            processed_at=datetime.utcnow()
        )
        
        # Update booking status
        booking.status = 'confirmed'
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment processed successfully',
            'payment': payment.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# About Us Route
@app.route('/api/about', methods=['GET'])
def get_about():
    try:
        about_sections = AboutUs.query.all()
        return jsonify([section.to_dict() for section in about_sections]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Peiris Grand Resort API is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)