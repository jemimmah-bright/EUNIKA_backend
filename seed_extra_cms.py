import json
from app import app
from models import db, Page, Section

def seed_extra_cms():
    with app.app_context():
        # Initiatives Sections
        initiatives_sections = [
            {
                'section_name': 'Header',
                'section_type': 'header',
                'content': {
                    'title': 'Our Initiatives',
                    'subtitle': 'Our work is delivered through focused initiatives designed to address specific community needs while advancing a shared mission.'
                }
            },
            {
                'section_name': 'Programs',
                'section_type': 'program',
                'content': {
                    'title_1': 'Mikka Parents School',
                    'tag_1': 'Educating vulnerable children for a brighter and dignified future',
                    'desc_1': 'An education-focused initiative designed to provide holistic, quality learning opportunities for vulnerable children, including those from disadvantaged and refugee backgrounds.',
                    'img_1': 'https://picsum.photos/seed/mikka/800/600',
                    
                    'title_2': 'Agriscale Initiative',
                    'tag_2': 'Empowering women and girls to grow sustainable livelihoods',
                    'desc_2': 'Designed for empowering women and girls with smart farming skills, agribusiness knowledge, and market access to strengthen livelihoods.',
                    'img_2': 'https://picsum.photos/seed/agri/800/600',
                    
                    'title_3': 'CollectivelyChristians.com',
                    'tag_3': 'Building empowered, self-reliant Christian communities',
                    'desc_3': 'A social enterprise dedicated to empowering Christian communities through skills development, economic initiatives, and collaborative events.',
                    'img_3': 'https://picsum.photos/seed/christian/800/600',
                    
                    'title_4': 'Kilimani Innovation Hub',
                    'tag_4': 'Shaping young innovators to create solutions that matter',
                    'desc_4': 'An innovation and entrepreneurship hub nurturing visionary young entrepreneurs by providing mentorship, skills training, and a supportive environment.',
                    'img_4': 'https://picsum.photos/seed/hub/800/600',
                    
                    'title_5': 'Hope Harbingers International',
                    'tag_5': 'Responding with hope when crisis strikes',
                    'desc_5': 'A humanitarian response initiative focused on delivering rapid, life-saving support to communities affected by war, crisis, and disasters across Africa.',
                    'img_5': 'https://picsum.photos/seed/hope/800/600',
                    
                    'title_6': 'Cycle of Care',
                    'tag_6': 'Restoring dignity, protecting health, and empowering girls',
                    'desc_6': 'A community health and dignity initiative focused on advancing sexual and reproductive health rights and ensuring access to menstrual health education.',
                    'img_6': 'https://picsum.photos/seed/care/800/600'
                }
            },
            {
                'section_name': 'CTA',
                'section_type': 'cta',
                'content': {
                    'title': 'Want to support a specific initiative?',
                    'desc': 'We welcome partners for individual projects and long-term programs.'
                }
            }
        ]

        # Partnership Sections
        partnership_sections = [
            {
                'section_name': 'Header',
                'section_type': 'header',
                'content': {
                    'title': 'Working Together <br/><span class="text-brandGreen">for Impact</span>',
                    'subtitle': 'Partnerships are central to how we deliver sustainable, community-driven solutions. We work with aligned partners to co-create impact.'
                }
            },
            {
                'section_name': 'Partner Models',
                'section_type': 'models',
                'content': {
                    'model1_title': 'Development Partners',
                    'model1_desc': 'To design, fund, and scale high impact programs.',
                    'model2_title': 'Government & Institutions',
                    'model2_desc': 'To align initiatives with national and local development priorities.',
                    'model3_title': 'Community Organizations',
                    'model3_desc': 'To ensure locally led, culturally relevant, and inclusive implementation.',
                    'model4_title': 'Private Sector Partners',
                    'model4_desc': 'To drive innovation, market access, and sustainable financing models.',
                    'model5_title': 'Religious Institutions',
                    'model5_desc': 'To design programs that impact their members of their ministries.'
                }
            },
            {
                'section_name': 'Why Partner',
                'section_type': 'cta',
                'content': {
                    'benefit1': 'Trusted local implementation partner',
                    'benefit2': 'Community driven and impact focused approach',
                    'benefit3': 'Transparent and accountable systems',
                    'benefit4': 'Flexible collaboration models'
                }
            }
        ]

        # Team Sections
        team_sections = [
            {
                'section_name': 'Header',
                'section_type': 'header',
                'content': {
                    'title': 'Leadership & Team',
                    'subtitle': 'Eunikare International is led by a dedicated team of professionals committed to social transformation and community excellence.'
                }
            },
            {
                'section_name': 'Board',
                'section_type': 'board',
                'content': {
                    'm1_name': 'Edward Mwaka Oola', 'm1_role': 'Chairperson', 'm1_image': 'https://picsum.photos/seed/e1/300/300',
                    'm2_name': 'Anita Malinga', 'm2_role': 'Vice Chairperson', 'm2_image': 'https://picsum.photos/seed/e2/300/300',
                    'm3_name': 'Davis Wambongo', 'm3_role': 'Treasurer', 'm3_image': 'https://picsum.photos/seed/e3/300/300',
                    'm4_name': 'Liven Nagawa', 'm4_role': 'Company Secretary', 'm4_image': 'https://picsum.photos/seed/e4/300/300'
                }
            },
            {
                'section_name': 'Senior Management',
                'section_type': 'management',
                'content': {
                    'm1_name': 'Eunice Acan', 'm1_role': 'CEO', 'm1_image': 'https://picsum.photos/seed/e5/300/300',
                    'm2_name': 'Abert', 'm2_role': 'Director of Programs', 'm2_image': 'https://picsum.photos/seed/e6/300/300'
                }
            },
            {
                'section_name': 'Program Managers',
                'section_type': 'managers',
                'content': {
                    'm1_name': 'Sharon O', 'm1_role': 'Finance Manager', 'm1_image': 'https://picsum.photos/seed/e7/300/300',
                    'm2_name': 'Angela', 'm2_role': 'Partnerships & Resource Mobilization', 'm2_image': 'https://picsum.photos/seed/e8/300/300',
                    'm3_name': 'David', 'm3_role': 'Communications & Advocacy', 'm3_image': 'https://picsum.photos/seed/e9/300/300',
                    'm4_name': 'Ambrose', 'm4_role': 'MEL Officer', 'm4_image': 'https://picsum.photos/seed/e10/300/300'
                }
            }
        ]

        # News Sections
        news_sections = [
            {
                'section_name': 'Header',
                'section_type': 'header',
                'content': {
                    'title': 'News & Insights',
                    'subtitle': 'Stories, opportunities, and updates from our work across communities in Uganda.'
                }
            },
            {
                'section_name': 'Posts',
                'section_type': 'posts',
                'content': {
                    'p1_date': 'MARCH 15, 2024', 'p1_author': 'ADMIN', 'p1_title': 'YELEP Cohort 5 Now Open Applications', 'p1_desc': 'The Youth Empowered Leadership and Entrepreneurship Program returns for its fifth cohort in partnership with Shine Leadership International....', 'p1_img': 'https://picsum.photos/seed/news1/600/400',
                    'p2_date': 'MARCH 10, 2024', 'p2_author': 'ADMIN', 'p2_title': 'Call for Volunteers and Program Directors', 'p2_desc': 'Are you passionate about serving communities in Uganda? We are inviting experienced individuals to lead initiatives across our six focus areas.', 'p2_img': 'https://picsum.photos/seed/news2/600/400',
                    'p3_date': 'FEBRUARY 28, 2024', 'p3_author': 'ADMIN', 'p3_title': 'How Youth Champions Are Transforming Lives', 'p3_desc': 'Through the YELEP program, young leaders mobilized resources to support Christine Nazziwa, a single mother of six and survivor of domestic violence.', 'p3_img': 'https://picsum.photos/seed/news3/600/400',
                    'p4_date': 'FEBRUARY 20, 2024', 'p4_author': 'ADMIN', 'p4_title': 'Maama Mikka Appeal Improving Conditions', 'p4_desc': 'Children at Mikka Parent School need safe learning environments. We are mobilizing resources to repair classrooms and renovate dormitories.', 'p4_img': 'https://picsum.photos/seed/news4/600/400'
                }
            }
        ]

        pages_data = {
            '/initiatives': initiatives_sections,
            '/partnership': partnership_sections,
            '/team': team_sections,
            '/news': news_sections
        }

        for slug, sections in pages_data.items():
            page = Page.query.filter_by(slug=slug).first()
            if page:
                for old_section in page.sections:
                    db.session.delete(old_section)
                
                for idx, s in enumerate(sections):
                    new_sec = Section(
                        page_id=page.id,
                        section_name=s['section_name'],
                        section_type=s['section_type'],
                        content_json=json.dumps(s['content']),
                        order=idx
                    )
                    db.session.add(new_sec)

        db.session.commit()
        print("Successfully seeded extra CMS content!")

if __name__ == '__main__':
    seed_extra_cms()
