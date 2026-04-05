# Roofmate Django Website (Multi-page Version)

A professional roofing website starter built with:
- HTML templates
- CSS
- Bootstrap 5
- Django backend

## Included pages
- Home
- About Us
- Our Projects
- Gallery
- Blog
- Contact / enquiry form
- Floating enquiry chatbot on all pages

## Backend features
- Django enquiry form saving submissions to SQLite
- Admin panel for enquiries, projects, gallery items and blog posts
- Simple chatbot endpoint for common service questions
- Multi-page routing for a more complete business website structure

## Run locally

```bash
python -m venv venv
# Windows
venv\Scriptsctivate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Homepage: http://127.0.0.1:8000/
- About: http://127.0.0.1:8000/about/
- Projects: http://127.0.0.1:8000/projects/
- Gallery: http://127.0.0.1:8000/gallery/
- Blog: http://127.0.0.1:8000/blog/
- Contact: http://127.0.0.1:8000/contact/
- Admin: http://127.0.0.1:8000/admin/

## Notes
- The design uses online placeholder images from Unsplash for demo presentation.
- Replace company phone, email and images with real Roofmate details.
- Projects, gallery items and blog posts can be managed in Django admin.
