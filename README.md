# 🤖 Jetson AI Research Lab - Community Automations

<div align="center">

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/invite/6wG2rkVqdU)
[![n8n](https://img.shields.io/badge/n8n-Workflows-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

**Supercharge your AI research community with powerful Discord automations and workflows!**

[Features](#-features) • [Quick Start](#-quick-start) • [Workflows](#-available-workflows) • [Join Discord](#-join-our-community)

</div>

---

## 📖 About

Welcome to the **Jetson AI Research Lab Community Automations** repository! This project provides a collection of n8n workflows and Discord bot automations designed to enhance collaboration, productivity, and engagement within the Jetson AI Research community.

Whether you're looking to automate daily AI digests, integrate smart home devices, or streamline community interactions, this repository has you covered.

## ✨ Features

- 🔄 **Pre-built n8n Workflows** - Ready-to-use automation flows for common tasks
- 🐳 **Docker Setup** - Easy local deployment with Docker Compose
- 🤝 **Community-Driven** - Built by the community, for the community
- 🚀 **Easy to Extend** - Add your own workflows and automations
- 📊 **Discord Integration** - Seamless Discord bot automations (coming soon!)

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed
- Basic understanding of n8n (helpful but not required)

### Setup in 3 Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/OriNachum/jetson-community-automations.git
   cd jetson-community-automations
   ```

2. **Set up your environment**
   ```bash
   cd docker
   cp .env.example .env
   # Edit .env and set your POSTGRES_PASSWORD
   ```

3. **Start n8n**
   ```bash
   docker-compose up -d
   ```

   Access n8n at `http://localhost:5678` 🎉

> 📚 For detailed setup instructions, see the [Docker Setup Guide](docker/README.md)

## 📁 Repository Structure

```
jetson-community-automations/
├── flows/              # n8n workflow files
│   ├── daily-ai-digest/    # Daily AI news digest automation
│   └── sensibo/            # Sensibo smart device integration
├── docker/             # Docker setup for local n8n instance
│   ├── docker-compose.yml
│   ├── .env.example
│   └── README.md
└── bots/               # Discord bot automations (coming soon!)
```

## 🔧 Available Workflows

### 📰 Daily AI Digest
Automatically curate and share daily AI news, research updates, and community highlights to keep everyone informed.

### 🌡️ Sensibo Integration
Smart home automation workflows for climate control and environmental monitoring within the research lab.

### 🔜 Coming Soon
- Discord moderation automation
- Community event scheduler
- Research paper tracker
- AI model deployment notifications

## 🤝 Join Our Community

Ready to collaborate with AI researchers and enthusiasts?

<div align="center">

### [**Join the Jetson AI Research Lab Discord →**](https://discord.com/invite/6wG2rkVqdU)

Connect with fellow researchers, share your projects, and get help from the community!

</div>

## 💡 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Share your workflows** - Built something cool? Submit a PR!
2. **Report bugs** - Found an issue? Open a GitHub issue
3. **Improve documentation** - Help others get started faster
4. **Join discussions** - Share ideas in our Discord server

### Adding Your Workflow

1. Fork the repository
2. Create a new folder in `flows/` with your workflow name
3. Export your n8n workflow as JSON and add it to your folder
4. Include a README explaining what it does
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with ❤️ by the Jetson AI Research Lab community. Special thanks to all contributors and community members who make this project possible!

---

<div align="center">

**[⭐ Star this repo](https://github.com/OriNachum/jetson-community-automations)** if you find it useful!

Made with 🤖 for the AI research community

</div>