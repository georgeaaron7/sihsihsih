# Video and Image Assets

This directory contains the media assets for the Argo Float Dashboard.

## Required Files

### Background Video
- `ocean-background.mp4` - Main background video for the landing page
  - Recommended: 1080p or higher resolution
  - Duration: 10-30 seconds (will loop)
  - Format: MP4 (H.264 codec for broad compatibility)
  - File size: Keep under 10MB for optimal loading

### Poster Images
- `ocean-poster.jpg` - High-quality poster frame from the video
  - Resolution: Same as video resolution
  - Format: JPEG, optimized for web
  - Use case: Shown while video loads and as fallback

- `ocean-poster-blur.jpg` - Blurred, low-resolution version
  - Resolution: 50-100px wide (will be scaled up)
  - Heavy blur applied for placeholder effect  
  - File size: Under 50KB
  - Use case: Immediate placeholder while high-res content loads

## Adding Your Own Assets

1. Place your video file as `ocean-background.mp4`
2. Create a poster frame as `ocean-poster.jpg` 
3. Create a blurred version as `ocean-poster-blur.jpg`
4. Update the `LandingHero` component props if using different filenames

## Sample Assets

For development purposes, you can use any ocean/water video. Some suggestions:

- Stock footage from Pexels, Unsplash, or Pixabay
- Nature documentaries (with proper licensing)
- Generated placeholder video using tools like FFmpeg

## Optimization Tips

- Use a video hosting service (Vimeo, YouTube) for larger files
- Consider WebM format as well for better compression
- Test autoplay behavior across different browsers
- Ensure video works well on mobile devices
