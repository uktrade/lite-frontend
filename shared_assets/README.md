# LITE Shared Assets

LITE Shared Assets contains the code and assets you need to start building a consistent user interface for LITE services.

## Installation

Add the project as a submodule in your repository, then add an import in your main scss file like so: ```@import "../../lite-shared-assets/lite-frontend/scss/all";```

## Components

### Buttons

Icon Button

### Modals

Styling for modals

### Search

Search bar

### Tabs

Lightweight alternative to the GOV.UK Design System tab bar

### User Account

Styling for log out, divider and user account menu in the nav bar.

## SVG Icons

The LITE projects use SVGs for icons. This has several benefits:

* Infinite scalability
* Smaller size
* Ability to recolour

#### To use LITE SVGs in your project:

Add ```os.path.join(BASE_DIR, 'lite-shared-assets/lite-frontend/assets/images'),``` to ```SVG_DIRS``` in your settings file.

This requires [django-inline-svg](https://github.com/mixxorz/django-inline-svg).
