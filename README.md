# NIIT Connect

A modern, responsive Django-based social platform designed for students to connect, share posts, and interact within a learning community. NIIT Connect features a sleek glassmorphism UI, a global feed, direct messaging, and a comprehensive administrative dashboard.

## Features

- **Authentication & User Management**: Secure registration, login, and password management.
- **Student Profiles**: Customizable profiles with avatars, bios, and program details.
- **Global AJAX Profile Modal**: View any user's profile instantly without leaving the current page.
- **Social Feed**: Create and view posts with text, image attachments, and links.
- **Direct Messaging**: One-on-one chat interface with a dedicated inbox.
- **Admin Dashboard**: Analytics, metrics, and tools for managing users and platform activity.
- **Modern UI/UX**: Fully responsive, clean aesthetic utilizing CSS glassmorphism, floating input labels, and fluid layouts.

## Tech Stack

- **Backend**: Python, Django 6.0
- **Database**: SQLite (default, easily adaptable to PostgreSQL)
- **Frontend**: HTML5, Vanilla CSS3, Vanilla JavaScript
- **Static File Serving**: WhiteNoise

## Getting Started

Follow these steps to set up the project locally for development and testing.

### Prerequisites

- Python 3.10+
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd NIIT-Connect
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Project Structure

This project follows a global front-end structure for ease of development:

```text
NIIT-Connect/
├── accounts/          # Logic for authentication and user profiles
├── chats/             # Logic for direct messaging
├── dashboard/         # Logic for the admin panel and analytics
├── posts/             # Logic for creating and displaying posts
├── core/              # Global project settings and main URL routing
│
├── templates/         # Centralized HTML templates
│   ├── accounts/      # (login, profile settings, etc.)
│   ├── chats/         # (inbox, chat room)
│   ├── dashboard/     # (feed, admin dashboard, manage users)
│   └── base.html      # Base template containing global layout and modals
│
├── static/            # Centralized static assets
│   ├── css/           # Mirrored CSS structure (accounts, chats, dashboard, global.css)
│   └── images/        # Global images (logos, default avatars)
│
└── manage.py          # Django management script
```

## Usage

- **User Registration**: New users can register via the platform. After registering, they will be prompted to complete their profile (upload an avatar, set their program, etc.).
- **Global Feed**: Users can navigate to the dashboard to view posts from others and share their own updates.
- **Chat**: Users can click on another user's profile card or use the inbox to start a direct message thread.
- **Admin**: Superusers can access the Admin Dashboard to view platform statistics and manage user accounts.

## Contributing

Contributions, issues, and feature requests are welcome! 

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License.
