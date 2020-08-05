# LITE Shared Assets

LITE Shared Assets contains the code and assets you need to start building a consistent user interface for LITE services.

## Installation

Add the project as a submodule in your repository, then add an import in your main scss file like so: ```@import "../../lite-shared-assets/lite-frontend/scss/all";```

## Linting

To run linting: `npx sass-lint -v`

## To use LITE SVGs in your project:

Add ```os.path.join(BASE_DIR, 'lite-shared-assets/lite-frontend/assets/images'),``` to ```SVG_DIRS``` in your settings file.

This requires [django-inline-svg](https://github.com/mixxorz/django-inline-svg).
