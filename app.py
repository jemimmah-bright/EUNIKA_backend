from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Inquiry, AdminUser, SiteSettings, ContentBlock, ImageAsset
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Enable CORS for all routes (to allow React to communicate with this API)
CORS(app)

# Configure the SQLAlchemy connection to the local XAMPP MySQL database
# User: root, Password: (empty), Host: localhost, Database: eunika_db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/eunika_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret-eunika-key'

db.init_app(app)

@app.route('/api/inquiries', methods=['POST'])
def create_inquiry():
    data = request.get_json()
    
    # Simple validation
    if not data or not data.get('full_name') or not data.get('email') or not data.get('message'):
        return jsonify({'error': 'Missing required fields: full_name, email, or message'}), 400

    try:
        new_inquiry = Inquiry(
            full_name=data.get('full_name'),
            email=data.get('email'),
            interest_area=data.get('interest_area', 'Other'),
            message=data.get('message')
        )
        db.session.add(new_inquiry)
        db.session.commit()
        return jsonify({'message': 'Inquiry successfully saved!', 'data': new_inquiry.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ================= CMS ENDPOINTS =================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = AdminUser.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful', 'token': 'dummy-token-for-now'})
    elif username == 'admin' and password == 'password':
        # Default fallback admin
        return jsonify({'message': 'Login successful', 'token': 'dummy-token-for-now'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/settings', methods=['GET'])
def get_settings():
    settings = SiteSettings.query.all()
    # Return as an object for easy access
    result = {s.setting_key: s.setting_value for s in settings}
    return jsonify(result)

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    data = request.get_json()
    for key, value in data.items():
        setting = SiteSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
        else:
            new_setting = SiteSettings(setting_key=key, setting_value=value)
            db.session.add(new_setting)
    try:
        db.session.commit()
        return jsonify({'message': 'Settings updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/content', methods=['GET'])
def get_content():
    blocks = ContentBlock.query.all()
    result = {b.block_key: b.content_text for b in blocks}
    return jsonify(result)

@app.route('/api/content', methods=['PUT'])
def update_content():
    data = request.get_json()
    for key, value in data.items():
        block = ContentBlock.query.filter_by(block_key=key).first()
        if block:
            block.content_text = value
        else:
            new_block = ContentBlock(block_key=key, content_text=value)
            db.session.add(new_block)
    try:
        db.session.commit()
        return jsonify({'message': 'Content updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    asset_key = request.form.get('asset_key')
    
    if file.filename == '' or not asset_key:
        return jsonify({'error': 'No selected file or missing asset_key'}), 400
        
    filename = secure_filename(file.filename)
    # prepend timestamp to avoid collisions
    import time
    filename = f"{int(time.time())}_{filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Save to db
    asset = ImageAsset.query.filter_by(asset_key=asset_key).first()
    if asset: # delete old file potentially? for now just update path
        asset.file_path = filename
    else:
        asset = ImageAsset(asset_key=asset_key, file_path=filename)
        db.session.add(asset)
        
    try:
        db.session.commit()
        return jsonify({'message': 'File uploaded', 'asset': asset.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/assets', methods=['GET'])
def get_assets():
    assets = ImageAsset.query.all()
    result = {a.asset_key: a.to_dict()['url'] for a in assets}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
