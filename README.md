# GitDocs

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-13+-000000.svg?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

**GitDocs** transforms GitHub repositories into polished technical blog posts using AI.

## 🎥 **I'll be releasing a video soon** showcasing the tool and walking through how to use it effectively.


## 🌟 Features

- **One-Click Blog Generation**: Enter a GitHub repo URL, get a complete technical blog post
- **Smart Repository Analysis**: Automatically detects tech stack, parses README, and extracts meaningful code snippets
- **AI-Powered Content**: Leverages modern language models to create coherent, informative technical content
- **Clean NextJS Frontend**: Modern responsive interface built with NextJS and Tailwind CSS
- **Local Fallback**: Continues to function even when AI services are unavailable

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AnishMane/GitDocs.git
   cd GitDocs
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

4. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
    cd backend
    python -u app.py
   ```
   The backend will be available at http://localhost:5000

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```
   The application will be available at http://localhost:3000

## 🔧 How It Works

GitDocs operates in three main stages:

1. **Repository Analysis**:
   - Clones the target repository
   - Identifies technology stack based on file extensions and dependencies
   - Extracts README content and representative code snippets

2. **Content Generation**:
   - Sends repository metadata to AI model via OpenRouter API
   - Structures blog with sections for introduction, features, technical details, and code examples
   - Falls back to template-based generation if API is unavailable

3. **Presentation**:
   - Renders Markdown blog content with syntax highlighting
   - Provides download and copy options

## 📚 API Documentation

### Generate Blog

```
POST /generate-blog
```

**Request Body**:
```json
{
  "repo_url": "https://github.com/AnishMane/GitDocs"
}
```

**Response**:
```json
{
  "blog": "# Generated Markdown Content..."
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenRouter API for AI integration
- NextJS and Flask communities for excellent documentation
- All the open-source libraries that made this project possible
