# Zaitouna

![zairouna responsive screenshot](readme/am_i_responsive.png)

## Introduction

Zaitouna is a recipe Website and the name "Zaitouna" means olive in Arabic, symbolizing health and flavor, invoking the essence of olive and the rich flavors it represents in Arabic cuisine. Zaitouna has been developed as part of the Code Institute's Full-Stack Developer course as my 4th project - focusing on Django and Bootstrap frameworks, Database manipulation and CRUD functionality. 


View the live site here : [Zaitouna](https://zaitouna-rano-19b1e34433ec.herokuapp.com/)  
  
For Admin access with relevant sign-in information: [Zaitouna Admin](https://zaitouna-rano-19b1e34433ec.herokuapp.com/admin/)  

<hr>

## Table of Contents

- [Zaitouna](#Zaitouna)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
- [UX - User Experience](#ux---user-experience)
  - [Design Inspiration](#design-inspiration)
    - [Colour Scheme](#colour-scheme)
    - [Font](#font)
- [Project Planning](#project-planning)
  - [Strategy Plane](#strategy-plane)
    - [Site Goals](#site-goals)
  - [Agile Methodologies - Project Management](#agile-methodologies---project-management)
    - [MoSCoW Prioritization](#moscow-prioritization)
    - [Sprints](#sprints)
  - [User Stories](#user-stories)
    - [Visitor User Stories](#visitor-user-stories)
    - [Epic - User Profile](#epic---user-profile)
    - [Epic - Articles](#epic---articles)
    - [Epic - Booking](#epic---booking)
    - [Epic - Photo Gallery](#epic---photo-gallery)
    - [Epic - Visit Us/Reviews](#epic---visit-usreviews)
  - [Scope Plane](#scope-plane)
  - [Structural Plane](#structural-plane)
  - [Skeleton \& Surface Planes](#skeleton--surface-planes)
    - [Wireframes](#wireframes)
    - [Database Schema - Entity Relationship Diagram](#database-schema---entity-relationship-diagram)
    - [Security](#security)
- [Features](#features)
  - [User View - Registered/Unregistered](#user-view---registeredunregistered)
  - [CRUD Functionality](#crud-functionality)
  - [Feature Showcase](#feature-showcase)
  - [Future Features](#future-features)
- [Technologies \& Languages Used](#technologies--languages-used)
  - [Libraries \& Frameworks](#libraries--frameworks)
  - [Tools \& Programs](#tools--programs)
- [Testing](#testing)
- [Deployment](#deployment)
  - [Connecting to GitHub](#connecting-to-github)
  - [Django Project Setup](#django-project-setup)
  - [Cloudinary API](#cloudinary-api)
  - [Elephant SQL](#elephant-sql)
  - [Heroku deployment](#heroku-deployment)
  - [Clone project](#clone-project)
  - [Fork Project](#fork-project)
- [Credits](#credits)
  - [Code](#code)
  - [Media](#media)
    - [Additional reading/tutorials/books/blogs](#additional-readingtutorialsbooksblogs)
  - [Acknowledgements](#acknowledgements)


## Overview

Zaitouna is a recipe Website that represents Arabic cuisine. Users are invited to:

- Join the Zaitouna Website
- Create their own profiles
- Update their Profiles 
- Interact with Website recipes
- Create and manage their recipes
- Share their thoughts as Comments 
- Save the recipe for later reach as a bookmark
- Share the recipe over social media accounts

Zaitouna is accessible via all browsers with full responsiveness on different screen sizes. The objective of the project is to develop a comprehensive recipe website where users can discover, save, and share recipes. The website aims to provide a user-friendly platform for individuals interested in cooking to find a wide range of recipes and cooking difficulty levels. Additionally, the website will facilitate interaction and engagement among users through features such as commenting, rating, and sharing recipes.


# UX - User Experience

## Design Inspiration

The design inspiration behind the Zaitouna website is rooted in creating a visually appealing and comfortable user experience. With a focus on olives, symbolized by the name "Zaitouna" which means olives in Arabic, the design aims to evoke a sense of freshness, tranquility, and authenticity.

The choice of a white background contributes to a clean and minimalist aesthetic, providing a canvas for the vibrant green color scheme to shine. Green, reminiscent of olive leaves, is prominently featured throughout the website to reinforce the connection to nature and the Mediterranean region.

The logo, with its depiction of olive leaves, serves as a visual representation of the website's name and theme. By incorporating elements from nature, the logo reinforces the concept of freshness and natural ingredients.

<img src="readme/logo.png" alt="Zaitouna logo" width="360" ><br>




### Colour Scheme

Colors have been selected carefully in a way that reflects the essence of olives.
**Primary Color (Header/Footer): #184B44**
This deep green shade represents the rich color of olives, tying in with the Mediterranean theme of the website.

**Accent Color: #FAD02E**
Our warm yellow accent color symbolizes the transformation of olives into delicious meals, mirroring the process from raw material to culinary delight.

**Secondary Accent Colors:**
#7DCE82: A refreshing mint green shade, perfect for buttons and interactive elements.

**Neutral Color**
#FFFFFF: Pure white is used to ensure readability and contrast against the other dark elements.


![colours](readme/color-schema.png)  

### Font

Using [Google Fonts](https://fonts.google.com/), two fonts was opted: 

**Chilanka:**

Chilanka font was opted for the text throughout the website. Its handwritten style evokes a sense of familiarity and nostalgia, reminiscent of jotting down recipes on paper. This choice aims to create a personal connection with users, inviting them to share their culinary creations as if they were writing them by hand.

**Montserrat:**

Montserrat is used for titles and headings, adding a touch of elegance and modernity to the website's design. Its clean and geometric appearance complements the handwritten style of Chilanka, creating a balanced and harmonious typographic palette.

In development, 'Chilanka' was identified by variable ``` --main-font```, whilst 'Montserrat' was set as ``` --title``` within the CSS file. Similar to my setup for the project's colors, using variables helped to speed up the front-end process.

  
![fonts](readme/font-type.png)  


# project-portfolio-4

Project Objective:
The objective of the project is to develop a comprehensive recipe website where users can discover, save, and share recipes. The website aims to provide a user-friendly platform for individuals interested in cooking to find a wide range of recipes and cooking difficulty levels. Additionally, the website will facilitate interaction and engagement among users through features such as commenting, rating, and sharing recipes.

Site User Goals:
Discover Recipes: Users want to find new and interesting recipes to try out.
Save and Organize Recipes: Users want to save their favorite recipes and organize them for easy access.
Interact with Community: Users want to engage with other users by sharing their experiences, leaving comments, and rating recipes.
Contribute Content: Users want to contribute their own recipes to the website and share them with others.
Learn and Improve Cooking Skills: Users want to learn new cooking techniques, discover tips, and improve their culinary skills through the content provided on the website.
Site Owner Goals:
Provide Valuable Content: The site owner aims to curate and provide a diverse range of high-quality recipes to attract and retain users.
Increase User Engagement: The site owner wants to foster a vibrant community where users actively interact with each other and contribute to the content.
Grow User Base: The site owner aims to attract a large user base by offering a user-friendly and feature-rich platform for recipe enthusiasts.
Generate Revenue: The site owner may have objectives related to generating revenue through advertising, sponsored content, premium features, or affiliate partnerships.
Maintain and Improve Website: The site owner aims to regularly maintain and improve the website to ensure optimal performance, usability, and security.
