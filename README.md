# Langchain FastAPI Streamlit Application

## Overview

This application uses OpenAI, Langchain, FastAPI, Chroma DB and Streamlit to offer a suite of tools for managing GitHub issues. The application provides the following features:

1. **GitHub Issue Generation**: Create GitHub issues from natural language descriptions.
2. **GitHub Issue Summarization**: Summarize GitHub issues for quick understanding.
3. **Q&A over GitHub Issues**: Perform question and answer sessions over GitHub issues using Retrieval Augmented Generation (RAG).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
  - [GitHub Issue Generation](#github-issue-generation)
  - [GitHub Issue Summarization](#github-issue-summarization)
  - [Q&A over GitHub Issues](#qa-over-github-issues)

## Installation

### Prerequisites

- Docker
- Docker Compose
- GitHub Personal Access Token

### Clone the Repository

```bash
git clone https://github.com/joshwizzy/team5-langchain-final-project
cd team5-langchain-final-project
```

### Configuration

To interact with the GitHub API and OpenAI services, you need to set up the appropriate API tokens. Follow the steps below to configure your environment.

1. **Generate GitHub Personal Access Token**

   - Log in to your GitHub account.
   - Navigate to **Settings** > **Developer settings** > **Personal access tokens**.
   - Click on **Generate new token** and select the required scopes for your application.
   - Copy the generated token.

2. **Generate OpenAI API Token**

   - Log in to your OpenAI account.
   - Navigate to **API Keys** and generate a new API key.
   - Copy the generated key.

3. **Set Environment Variables**
   - Create a `.env` file in the root directory of your project.
   - Add the following lines to the `.env` file:
     ```env
     GITHUB_TOKEN=your_personal_access_token
     OPENAI_API_TOKEN=your_openai_api_token
     GITHUB_REPOSITORY=githubusername/project
     ```

## Usage

### Running the Application

Using Docker Compose

- Ensure Docker and Docker Compose are installed on your machine.
- Navigate to the project directory.
- Build and run the containers:

```bash
docker-compose up --build
```

The FastAPI backend will be available at http://127.0.0.1:8000, and the Streamlit frontend will be available at http://localhost:8501.

### Stopping the Application

To stop the application, run:

```bash
docker-compose down
```

## Features

### GitHub Issue Generation

Transform natural language descriptions into GitHub issues. This feature helps in quickly creating well-structured issues from user inputs.

**Usage**

- Navigate to the "Generate Issue" section in the Streamlit app.
- Enter a natural language description of the issue.
- Click "Generate Issue".
  The generated issue will be displayed and can be directly posted to GitHub.

### GitHub Issue Summarization

Summarize existing GitHub issues for a concise overview. This feature helps in quickly understanding the essence of an issue without reading through long descriptions and comments.

**Usage**

- Navigate to the "Summarize Issue" section in the Streamlit app.
- Enter the GitHub issue ID in this format `username/reponame/issues/issue_number`.
- Click "Summarize Issue".
  The summary will be displayed.

### Q&A over GitHub Issues

Utilize Retrieval Augmented Generation (RAG) to perform Q&A sessions over GitHub issues. This feature enhances understanding and provides detailed answers based on the content of the issues.

**Usage**

- Navigate to the "Project Issues" section in the Streamlit app.
- Enter the GitHub project link in this format `username/reponame`.
- Click "Add repo".

  The app will display a loading indicator and load the issues.

Enter the question related to the fetched issues
