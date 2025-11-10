# Homepage Slideshow Setup Guide

## Overview
The homepage now features a dynamic slideshow that can be managed through the Django admin interface. This allows administrators to easily add, edit, and manage background images and content for the homepage hero section.

## Features
- **Dynamic Background Images**: Multiple slides with custom background images
- **Auto-advance**: Slides automatically change every 5 seconds
- **Navigation Dots**: Users can manually navigate between slides
- **Responsive Design**: Works seamlessly on all device sizes
- **Admin Management**: Full CRUD operations through Django admin
- **Fallback Support**: Falls back to default gradient if no slides are available

## Database Model
The `HomepageSlide` model includes the following fields:
- `title`: Main heading for the slide
- `subtitle`: Descriptive text below the title
- `image`: Background image for the slide
- `button_text`: Call-to-action button text (optional)
- `button_link`: URL for the call-to-action button (optional)
- `order`: Display order (lower numbers appear first)
- `is_active`: Whether the slide is currently active
- `created_at` & `updated_at`: Timestamps

## Admin Interface
Access the slideshow management through Django admin:
1. Navigate to `/admin/` in your browser
2. Login with admin credentials
3. Click on "Homepage Slides" under the "Core" section
4. Add, edit, or delete slides as needed

### Admin Features
- **List View**: Shows title, order, active status, and creation date
- **Filtering**: Filter by active status and creation date
- **Search**: Search by title and subtitle
- **Bulk Actions**: Change order and active status for multiple slides
- **Ordering**: Drag and drop functionality for easy reordering

## API Endpoint
The slides are served via REST API:
- **URL**: `/api/homepage-slides/`
- **Method**: GET
- **Response**: JSON array of active slides ordered by `order` field
- **Access**: Read-only (no authentication required)

## Frontend Implementation
The slideshow is implemented in `src/pages/Home.jsx`:
- Fetches slides from the API on component mount
- Auto-advances every 5 seconds when multiple slides exist
- Displays navigation dots for manual control
- Uses slide content (title, subtitle, button) when available
- Falls back to default content when no slides exist

## Sample Data
Sample slides have been created using the management command:
```bash
python manage.py create_sample_slides
```

## Adding Images
To add background images to slides:
1. Go to Django admin → Homepage Slides
2. Click on a slide to edit
3. Upload an image in the "Image" field
4. Save the slide

**Recommended Image Specifications:**
- **Resolution**: 1920x1080 or higher
- **Format**: JPG, PNG, or WebP
- **Aspect Ratio**: 16:9 (landscape)
- **File Size**: Under 2MB for optimal loading

## Customization
### Slide Duration
To change the auto-advance duration, modify the interval in `Home.jsx`:
```javascript
// Change from 5000ms (5 seconds) to desired duration
setInterval(() => {
  setCurrentSlide((prev) => (prev + 1) % slides.length);
}, 5000); // Change this value
```

### Transition Effects
The current implementation uses opacity transitions. To modify:
1. Update the CSS classes in the slide mapping
2. Adjust the `transition-opacity duration-1000` class

### Navigation Styling
Navigation dots can be customized by modifying the button classes in the navigation section.

## Troubleshooting

### Slides Not Appearing
1. Check if slides exist in Django admin
2. Verify slides are marked as "active"
3. Ensure the backend server is running
4. Check browser console for API errors

### Images Not Loading
1. Verify image files are uploaded correctly
2. Check Django media settings
3. Ensure proper file permissions
4. Verify CORS settings if needed

### Performance Issues
1. Optimize image file sizes
2. Consider using WebP format
3. Implement lazy loading if needed
4. Monitor API response times

## Future Enhancements
- **Video Backgrounds**: Support for video slides
- **Animation Effects**: Custom transition animations
- **Scheduling**: Time-based slide activation
- **Analytics**: Track slide engagement
- **A/B Testing**: Multiple slide variants

## Technical Notes
- The slideshow uses React hooks for state management
- Images are served through Django's media handling
- The component is fully responsive using Tailwind CSS
- Accessibility features include proper alt text and keyboard navigation