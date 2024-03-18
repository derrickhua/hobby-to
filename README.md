# HOBBY.TO

Welcome to the Hobby App project! This application is designed to help adults find new hobbies and activities in their city, providing an interactive platform to explore, track, and share their hobby journeys.

For an in-depth look at how this project was set up and to follow its development, check out our [Notion page](https://silken-muenster-22d.notion.site/Hobby-App-7173d65e38fd43b7949e2f1458d3fa41).

## Overview

HOBBY.TO allows users to discover hobbies through a searchable map and categorized listings. It provides details on each hobby, including cost, popularity, and how to get started. 
Users can also create and share their own hobby roadmaps, contributing to a community-driven database of hobby guides.

## Technology Stack Refined

- **SvelteKit**: Frontend framework for crafting the user interface, ensuring a modern, responsive design.
- **Flask**: Backend framework to manage API requests, serving as the intermediary between the frontend, Redis, and PostgreSQL databases.
- **Redis**: Utilized primarily for caching frequently accessed data and session management, enhancing the responsiveness of the application.
- **PostgreSQL**: The primary database for storing structured data such as user information, hobby details, and roadmaps. Its relational nature is ideal for complex queries and managing relationships between different data types.
- **Shadcn UI**: UI component library for SvelteKit, enabling rapid development of a polished user interface.
- **Leaflet**: A JavaScript library for adding interactive maps, essential for visualizing hobbies geographically.

## Features

### Homepage

- **Search Bar**: Enables users to search for hobbies by keywords or names within a specific city.
- **Interactive Map with Pins**: Displays hobbies geographically across the city using Leaflet. Users can interact with pins to discover new hobbies and locations.
- **List of Categories**: Allows users to browse hobbies by categories. Selecting a category filters both the map pins and search results.

### Hobby Details and Interaction

- **Pin Information Cards**: Clicking on a map pin opens a small card displaying the location's costs, and a link to their website.

## Future Plans

- **Recommendations Tab**: A feature to recommend locations to users based on their interests and past activities.
- - **Hobby Roadmaps/Pathways**: Users can view detailed guides on progressing in specific hobbies, including steps, resources, and community tips.
- **Sharing Roadmaps**: Users can contribute their own roadmaps, sharing their progression and tips with the community.
- **Login/Signup**: Secure authentication system for users to create and access their accounts. Supports OAuth for convenience.
- **Personal Dashboard**: A personalized area where users can track their hobby progress, manage roadmaps, and view their tried and tested hobbies and favorite places.
- **Tracking Personal Hobby Roadmaps**: Users can save and monitor their progress on various hobby roadmaps, marking steps as completed.
- **Creating and Sharing Personal Roadmaps**: Allows users to create personal roadmaps for hobbies they are knowledgeable about, sharing these with the community.
- **List of Hobbies Tried and Tested**: Users can maintain a list of hobbies they have explored, including notes on their experiences.
- **Favorite Places**: Enables users to bookmark places related to their hobbies for future reference, integrated with the map for visual tracking.
