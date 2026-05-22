from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Inquiry, AdminUser, SiteSettings, ContentBlock, ImageAsset, Page, Section
import pymysql
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Enable CORS for all routes (to allow React to communicate with this API)
CORS(app)

# Configure the SQLAlchemy connection
# Using SQLite for immediate reliability
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eunika.db'
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

@app.route('/api/admins', methods=['POST'])
def create_admin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
        
    existing_user = AdminUser.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
        
    new_admin = AdminUser(username=username)
    new_admin.set_password(password)
    
    db.session.add(new_admin)
    try:
        db.session.commit()
        return jsonify({'message': 'Admin user created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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

# ================= PAGE & SECTION ENDPOINTS =================

@app.route('/api/pages', methods=['GET'])
def get_pages():
    pages = Page.query.all()
    return jsonify([p.to_dict() for p in pages])

@app.route('/api/pages', methods=['POST'])
def create_page():
    data = request.get_json()
    new_page = Page(
        title=data.get('title'),
        slug=data.get('slug'),
        meta_description=data.get('meta_description'),
        status=data.get('status', 'Published')
    )
    db.session.add(new_page)
    db.session.commit()
    return jsonify(new_page.to_dict()), 201

@app.route('/api/pages/<int:page_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_page(page_id):
    page = Page.query.get_or_404(page_id)
    if request.method == 'GET':
        return jsonify(page.to_dict())
    if request.method == 'DELETE':
        db.session.delete(page)
        db.session.commit()
        return jsonify({'message': 'Page deleted'})
    
    data = request.get_json()
    page.title = data.get('title', page.title)
    page.slug = data.get('slug', page.slug)
    page.meta_description = data.get('meta_description', page.meta_description)
    page.status = data.get('status', page.status)
    db.session.commit()
    return jsonify(page.to_dict())

@app.route('/api/sections', methods=['POST'])
def create_section():
    data = request.get_json()
    new_section = Section(
        page_id=data.get('page_id'),
        section_name=data.get('section_name'),
        section_type=data.get('section_type'),
        content_json=json.dumps(data.get('content', {})),
        order=data.get('order', 0)
    )
    db.session.add(new_section)
    db.session.commit()
    return jsonify(new_section.to_dict()), 201

@app.route('/api/sections/<int:section_id>', methods=['PUT', 'DELETE'])
def manage_section(section_id):
    section = Section.query.get_or_404(section_id)
    if request.method == 'DELETE':
        db.session.delete(section)
        db.session.commit()
        return jsonify({'message': 'Section deleted'})
    
    data = request.get_json()
    section.section_name = data.get('section_name', section.section_name)
    section.section_type = data.get('section_type', section.section_type)
    if 'content' in data:
        section.content_json = json.dumps(data.get('content'))
    section.order = data.get('order', section.order)
    db.session.commit()
    return jsonify(section.to_dict())

def seed_data():
    with app.app_context():
        # List of default pages to ensure exist
        default_pages = [
            {'title': 'Home', 'slug': '/', 'meta': 'Eunikare International is an umbrella organization dedicated to systemic community transformation.'},
            {'title': 'About Us', 'slug': '/about', 'meta': 'Learn about Eunikare International and our mission.'},
            {'title': 'Initiatives', 'slug': '/initiatives', 'meta': 'Our current programs in health, education, and innovation.'},
            {'title': 'Impact', 'slug': '/impact', 'meta': 'The measurable difference we make in Ugandan communities.'},
            {'title': 'Partnership', 'slug': '/partnership', 'meta': 'Join our network of innovators and leaders.'},
            {'title': 'Team', 'slug': '/team', 'meta': 'Meet the dedicated team behind Eunikare.'},
            {'title': 'News', 'slug': '/news', 'meta': 'Latest stories and updates from the field.'}
        ]

        for p_data in default_pages:
            existing = Page.query.filter_by(slug=p_data['slug']).first()
            if not existing:
                new_p = Page(title=p_data['title'], slug=p_data['slug'], meta_description=p_data['meta'], status='Published')
                db.session.add(new_p)
                db.session.flush()
                
                # Add specialized sections for Home
                if p_data['slug'] == '/':
                    # Hero
                    db.session.add(Section(page_id=new_p.id, section_name='Hero Section', section_type='hero', content_json=json.dumps({
                        'badge': 'Based in Uganda, Serving Africa',
                        'title': 'Empowering <br><span class="text-brandGreen italic">Potential</span>,<br>Restoring <span class="text-brandMauve">Dignity.</span>',
                        'subtitle': 'Eunikare International is an umbrella organization dedicated to systemic community transformation through health, education, and innovation.',
                        'image': ''
                    })))
                    # Philosophy
                    db.session.add(Section(page_id=new_p.id, section_name='Our Philosophy', section_type='philosophy', content_json=json.dumps({
                        'title': 'Sustainability is not an accident, it is designed.',
                        'description': 'We move beyond traditional aid. By focusing on entrepreneurship and vocational skills alongside basic needs, we ensure that every community we touch becomes an engine of its own growth.'
                    })))
                
                # Specialized sections for About
                elif p_data['slug'] == '/about':
                    db.session.add(Section(page_id=new_p.id, section_name='Header', section_type='header', content_json=json.dumps({
                        'title': 'About Us',
                        'subtitle': 'Eunikare International operates as an umbrella institution implementing multiple initiatives addressing diverse community needs.'
                    })))
                    db.session.add(Section(page_id=new_p.id, section_name='Who We Are', section_type='who', content_json=json.dumps({
                        'title': 'Who We Are',
                        'description': 'Eunikare International is a registered nonprofit organization in Uganda operating as an umbrella institution that implements multiple initiatives. The organization integrates education, health, entrepreneurship, and social innovation within a coordinated framework.'
                    })))

                # Impact Page
                elif p_data['slug'] == '/impact':
                    db.session.add(Section(page_id=new_p.id, section_name='Hero Section', section_type='header', content_json=json.dumps({
                        'eyebrow': 'Evidence of Change',
                        'title': 'Impact Defined.',
                        'subtitle': 'We measure our success not by the number of projects completed, but by the dignity restored and the systems changed.'
                    })))
                    db.session.add(Section(page_id=new_p.id, section_name='Key Pillars', section_type='pillars', content_json=json.dumps({
                        'economic_title': 'Livelihoods & Agribusiness',
                        'economic_desc': 'We enable individuals and groups to build sustainable livelihoods by improving access to skills, resources, and financial opportunities.',
                        'education_title': 'Education & Skills',
                        'education_desc': 'We believe education is the bedrock of progress. Our programs bridge the gap for vulnerable children and youth.',
                        'health_title': 'Health & Wellbeing',
                        'health_desc': 'We work to ensure that basic healthcare and wellness information reach the most remote communities.'
                    })))

                # Partnership Page
                elif p_data['slug'] == '/partnership':
                    db.session.add(Section(page_id=new_p.id, section_name='Hero Section', section_type='header', content_json=json.dumps({
                        'title': 'Working Together for Impact.',
                        'subtitle': 'Partnerships are central to how we deliver sustainable, community-driven solutions. We work with aligned partners to co-create impact.'
                    })))

                # Team Page
                elif p_data['slug'] == '/team':
                    db.session.add(Section(page_id=new_p.id, section_name='Hero Section', section_type='header', content_json=json.dumps({
                        'title': 'The Hearts & Minds Behind Eunikare.',
                        'subtitle': 'Our multidisciplinary team is united by a shared commitment to building resilient communities through innovation and dedication.'
                    })))

                # News Page
                elif p_data['slug'] == '/news':
                    db.session.add(Section(page_id=new_p.id, section_name='Hero Section', section_type='header', content_json=json.dumps({
                        'title': 'Insights & Updates.',
                        'subtitle': 'Stay informed about our latest projects, community stories, and the ongoing journey of restoring dignity.'
                    })))

                else:
                    # Default generic section for other pages
                    db.session.add(Section(page_id=new_p.id, section_name='Header', section_type='header', content_json=json.dumps({
                        'title': p_data['title'],
                        'subtitle': 'Discover how we are making a difference.',
                        'image': ''
                    })))
        
        db.session.commit()
        print("Database checked and high-quality prototype content restored.")

if __name__ == '__main__':
    seed_data()
    app.run(debug=True, port=5000)
