import json
from app import app
from models import db, Page, Section

def seed_full_cms():
    with app.app_context():
        # Home Page Sections
        home_sections = [
            {
                'section_name': 'Hero Section',
                'section_type': 'hero',
                'content': {
                    'badge': 'Based in Uganda, Serving Africa',
                    'title': 'Empowering <br><span class="text-brandGreen italic">Potential</span>,<br>Restoring <span class="text-brandMauve">Dignity.</span>',
                    'subtitle': 'Eunikare International is an umbrella organization dedicated to systemic community transformation through health, education, and innovation.',
                    'image': 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?q=80&w=2070&auto=format&fit=crop'
                }
            },
            {
                'section_name': 'Impact Stats',
                'section_type': 'stats',
                'content': {
                    'stat_1_num': '1,200+',
                    'stat_1_label': 'Children Educated',
                    'stat_2_num': '600+',
                    'stat_2_label': 'Women Empowered',
                    'stat_3_num': '15',
                    'stat_3_label': 'Communities Served',
                    'stat_4_num': '02',
                    'stat_4_label': 'Innovation Hubs'
                }
            },
            {
                'section_name': 'Strategic Framework',
                'section_type': 'framework',
                'content': {
                    'title': 'Holistic solutions for <br><span class="text-brandMauve">multidimensional</span> needs.',
                    'card1_title': 'Education & Schools',
                    'card1_desc': 'Quality learning for vulnerable children via Mikka Parent School.',
                    'card2_title': 'Women in Agribusiness',
                    'card2_desc': 'Smart farming and financial inclusion via Agriscale Initiative.',
                    'card3_title': 'Health & SRHR',
                    'card3_desc': 'Restoring dignity and health access through Cycle of Care.',
                    'card4_title': 'Innovation & Tech',
                    'card4_desc': 'Nurturing the next generation of social entrepreneurs at Kilimani Hub.'
                }
            },
            {
                'section_name': 'Our Philosophy',
                'section_type': 'philosophy',
                'content': {
                    'title': 'Sustainability is not an <br><span class="text-brandGreen italic">accident</span>, it is designed.',
                    'subtitle': 'We move beyond traditional aid. By focusing on entrepreneurship and vocational skills alongside basic needs, we ensure that every community we touch becomes an engine of its own growth.',
                    'image': 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?q=80&w=2070&auto=format&fit=crop',
                    'point1_title': 'Accountability',
                    'point1_desc': 'Transparent systems for every shilling received.',
                    'point2_title': 'Locally Led',
                    'point2_desc': 'Programs designed by those who live the reality.'
                }
            },
            {
                'section_name': 'Flagships',
                'section_type': 'flagships',
                'content': {
                    'title': 'Innovation in Action',
                    'item1_title': 'Mikka Parents School',
                    'item1_desc': 'Educating vulnerable children for a brighter and dignified future',
                    'item1_image': 'https://picsum.photos/seed/mikka/800/600',
                    'item2_title': 'Agriscale Initiative',
                    'item2_desc': 'Empowering women and girls to grow sustainable livelihoods',
                    'item2_image': 'https://picsum.photos/seed/agri/800/600',
                    'item3_title': 'CollectivelyChristians.com',
                    'item3_desc': 'Building empowered, self-reliant Christian communities',
                    'item3_image': 'https://picsum.photos/seed/christian/800/600'
                }
            },
            {
                'section_name': 'Partners',
                'section_type': 'partners',
                'content': {
                    'partner1': 'Shine Leadership Int',
                    'partner2': 'Itinga Education',
                    'partner3': 'CMHLIVE',
                    'partner4': 'Cinelab Akademie',
                    'partner5': 'GCP Foundation'
                }
            },
            {
                'section_name': 'Call To Action',
                'section_type': 'cta',
                'content': {
                    'title': 'Ready to make a <br><span class="text-brandBlack">tangible</span> difference?',
                    'subtitle': "Whether you're an individual, a corporate partner, or an institution, there is a place for you in our mission. Let's co-create a future where every life has equal value."
                }
            }
        ]

        # Impact Page Sections
        impact_sections = [
            {
                'section_name': 'Hero Section',
                'section_type': 'header',
                'content': {
                    'eyebrow': 'Evidence of Change',
                    'title': 'Impact <br><span class="text-brandGreen italic font-light">Defined.</span>',
                    'subtitle': 'We measure our success not by the number of projects completed, but by the dignity restored and the systems changed.',
                    'image': 'https://images.unsplash.com/photo-1524069290683-0457abfe42c3?q=80&w=2070&auto=format&fit=crop',
                    'badge_number': '15+',
                    'badge_text': 'Rural Districts Reached'
                }
            },
            {
                'section_name': 'SDG Alignment',
                'section_type': 'sdg',
                'content': {
                    'point1': 'Global Alignment with 7 UN SDGs',
                    'point2': 'Locally Led Intervention Design',
                    'point3': 'Transparent Financial Reporting'
                }
            },
            {
                'section_name': 'Core Spheres',
                'section_type': 'spheres',
                'content': {
                    'title': 'Multidimensional Change',
                    'sphere1_title': 'Economic Empowerment',
                    'sphere1_subtitle': 'Livelihoods & Agribusiness',
                    'sphere1_desc': 'We enable individuals and groups to build sustainable livelihoods by improving access to skills, resources, and financial opportunities.',
                    'sphere1_image': 'https://images.unsplash.com/photo-1590650516494-2c8e4a446d54?q=80&w=2070&auto=format&fit=crop',
                    'sphere1_stat1': 'Increased household income by 40%',
                    'sphere1_stat2': '13 active women-led group enterprises',
                    'sphere1_stat3': 'Robust financial inclusion & savings culture',
                    
                    'sphere2_title': 'Education & Skill Access',
                    'sphere2_subtitle': 'Holistic Learning Models',
                    'sphere2_desc': 'We expand access to quality education and practical skills for children, youth, and women who face systemic barriers.',
                    'sphere2_image': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=2073&auto=format&fit=crop',
                    'sphere2_stat1': '310+ children supported annually',
                    'sphere2_stat2': 'Vocational pathways for out-of-school youth',
                    'sphere2_stat3': '100% PLE First Grade performance',

                    'sphere3_title': 'Community Resilience',
                    'sphere3_subtitle': 'Humanitarian Response',
                    'sphere3_desc': 'We support communities to withstand and recover from social, economic, and humanitarian shocks.',
                    'sphere3_image': 'https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?q=80&w=2070&auto=format&fit=crop',
                    'sphere3_stat1': 'Rapid crisis response systems',
                    'sphere3_stat2': 'Vulnerability reduction programs',
                    'sphere3_stat3': 'Stronger local community governance',

                    'sphere4_title': 'Women & Youth Leadership',
                    'sphere4_subtitle': 'Social Innovation',
                    'sphere4_desc': 'We invest in women and young people as drivers of change. By building leadership capacity and confidence.',
                    'sphere4_image': 'https://images.unsplash.com/photo-1531206715517-5cd94ee91962?q=80&w=2070&auto=format&fit=crop',
                    'sphere4_stat1': 'Leadership training for 600+ women',
                    'sphere4_stat2': 'Youth-driven social enterprise incubator',
                    'sphere4_stat3': 'Inclusive community policy advocacy'
                }
            },
            {
                'section_name': 'Numerical Stats',
                'section_type': 'stats',
                'content': {
                    'title': 'The Pulse of <br/><span class="text-brandGreen">Our Impact.</span>',
                    'subtitle': 'Data driven results from 30 years of on-ground implementation.',
                    'enroll_num': '310+',
                    'enroll_label': 'Annual School Enrollments',
                    'groups_num': '13',
                    'groups_label': 'Women-led Business Groups',
                    'indirect_num': '600+',
                    'indirect_label': 'Indirect Beneficiaries',
                    'loans_num': '187',
                    'loans_label': 'Higher-Ed EduLoans Issued'
                }
            },
            {
                'section_name': 'Testimonial',
                'section_type': 'testimonial',
                'content': {
                    'quote': 'Impact is defined by <span class="text-brandGreen font-bold">lasting change</span>, not short-term outputs. We focus on strengthening people, systems, and communities.',
                    'name': 'Eunice Acan',
                    'role': 'CEO, Eunikare International'
                }
            },
            {
                'section_name': 'Final CTA',
                'section_type': 'cta',
                'content': {
                    'title': 'Ready to grow with us?',
                    'subtitle': 'Join us in designing and delivering solutions that restore dignity and build resilient communities across Uganda.'
                }
            }
        ]

        # About Page Sections
        about_sections = [
            {
                'section_name': 'Header',
                'section_type': 'header',
                'content': {
                    'title': 'About Us',
                    'subtitle': 'Eunikare International operates as an umbrella institution implementing multiple initiatives addressing diverse community needs within a coordinated framework.'
                }
            },
            {
                'section_name': 'Who We Are',
                'section_type': 'who',
                'content': {
                    'title': 'Who We Are',
                    'p1': 'Eunikare International is a registered nonprofit organization in Uganda operating as an umbrella institution that implements multiple initiatives. The organization integrates education, health, entrepreneurship, and social innovation within a coordinated framework to deliver sustainable and measurable impact.',
                    'p2': 'Through collaboration with communities, institutions, and development partners, Eunikare designs people-centered solutions that strengthen capacity, enhance resilience, and support long-term social and economic transformation.',
                    'image': 'https://picsum.photos/seed/about-team/800/600'
                }
            },
            {
                'section_name': 'Vision & Mission',
                'section_type': 'vision',
                'content': {
                    'vision_title': 'Vision',
                    'vision_text': 'A world where every life has equal value and where all people can access education and healthcare.',
                    'mission_title': 'Mission',
                    'mission_text': 'To empower vulnerable communities in Uganda through education, health, and economic opportunities.'
                }
            },
            {
                'section_name': 'Our Core Values',
                'section_type': 'values',
                'content': {
                    'title': 'Our Core Values',
                    'value1_title': 'Empowerment',
                    'value1_desc': 'We equip individuals with knowledge and resources to drive sustainable growth.',
                    'value2_title': 'Integrity',
                    'value2_desc': 'We uphold transparency, accountability, and ethical practices in all actions.',
                    'value3_title': 'Inclusivity',
                    'value3_desc': 'We ensure that no one is left behind, designing programs that embrace diversity.'
                }
            },
            {
                'section_name': 'Sustainable Development Goals',
                'section_type': 'sdg',
                'content': {
                    'title': 'Our Work Contributes to Global Goals',
                    'desc': 'Our initiatives align with the UN Sustainable Development Goals, ensuring every program drives measurable impact and supports community transformation.',
                    'goal1_num': '1', 'goal1_title': 'No Poverty', 'goal1_desc': 'Reducing poverty through women and youth economic empowerment initiatives.',
                    'goal2_num': '2', 'goal2_title': 'Zero Hunger', 'goal2_desc': 'Promoting food security through the Agriscale initiative.',
                    'goal3_num': '3', 'goal3_title': 'Good Health', 'goal3_desc': 'Improving community health and SRHR via Cycle of Care.',
                    'goal4_num': '4', 'goal4_title': 'Quality Education', 'goal4_desc': 'Providing access to holistic education through Mikka Parent.',
                    'goal5_num': '5', 'goal5_title': 'Gender Equality', 'goal5_desc': 'Empowering women and girls through leadership and skills.',
                    'goal6_num': '8', 'goal6_title': 'Decent Work', 'goal6_desc': 'Supporting entrepreneurship and business skills.',
                    'goal7_num': '17', 'goal7_title': 'Partnerships', 'goal7_desc': 'Building strategic partnerships with communities and institutions.'
                }
            }
        ]

        pages_data = {
            '/': home_sections,
            '/impact': impact_sections,
            '/about': about_sections
        }

        for slug, sections in pages_data.items():
            page = Page.query.filter_by(slug=slug).first()
            if page:
                # Clear old sections
                for old_section in page.sections:
                    db.session.delete(old_section)
                
                # Add new comprehensive sections
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
        print("Successfully seeded full CMS content for Home, Impact, and About!")

if __name__ == '__main__':
    seed_full_cms()
