# Argo Float Dashboard Frontend

A modern, responsive TypeScript React frontend for visualizing Argo oceanographic float data across the Indian Ocean. Built with Vite, Tailwind CSS, and Framer Motion for an optimal user experience.

## 🌊 Features

### Landing Page
- **Background Video**: Full-viewport ocean background with autoplay support and fallback handling
- **Logo Animation**: Lottie-powered animated logo with reduced-motion support
- **Progressive Enhancement**: Blurred placeholder images load first for optimal performance
- **Responsive Design**: Mobile-first approach with optimized layouts

### Interactive Dashboard
- **Float Visualization**: Grid and list views of active Argo floats
- **Real-time Data**: Live updates from FastAPI backend
- **Click Tracking**: Automatic logging of user interactions with floats
- **Advanced Filtering**: Filter by region, temperature range, and other parameters

### Float Detail Views
- **Comprehensive Data**: Detailed float information including profiles and time series
- **Interactive Charts**: Temperature and salinity visualizations (placeholder ready for chart library)
- **Profile Tables**: Sortable, paginated profile data

### Accessibility & Performance
- **Keyboard Navigation**: Full keyboard accessibility support
- **Screen Reader Support**: Semantic HTML and ARIA labels
- **Reduced Motion**: Respects `prefers-reduced-motion` preference
- **Code Splitting**: Lazy-loaded routes for optimal bundle size
- **Error Boundaries**: Graceful error handling with retry mechanisms

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Argo Float API server running (default: http://127.0.0.1:8061)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

## 🔧 Environment Configuration

Create a `.env` file with the following variables:

```env
# API Configuration - REQUIRED
VITE_API_BASE=http://127.0.0.1:8061

# Feature Flags - OPTIONAL
VITE_ENABLE_3D_CANVAS=false
VITE_ENABLE_ANALYTICS=false

# Environment
VITE_ENV=development
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_API_BASE` | Base URL for the FastAPI backend | `http://127.0.0.1:8061` | Yes |
| `VITE_ENABLE_3D_CANVAS` | Enable 3D canvas features | `false` | No |
| `VITE_ENABLE_ANALYTICS` | Enable analytics tracking | `false` | No |
| `VITE_ENV` | Environment identifier | `development` | No |

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ErrorBoundary.tsx    # Error boundary wrapper
│   ├── FloatList.tsx        # Float grid/list component
│   ├── Footer.tsx           # Site footer
│   ├── LandingHero.tsx      # Hero section with video/animation
│   ├── LoadingSpinner.tsx   # Loading states
│   └── Nav.tsx              # Navigation header
├── lib/                 # Utilities and API client
│   └── apiClient.ts         # Typed API client with retry logic
├── pages/               # Route components
│   ├── DashboardPage.tsx    # Main dashboard
│   ├── FloatDetailPage.tsx  # Individual float details
│   ├── LandingPage.tsx      # Landing/home page
│   └── StatsPage.tsx        # Statistics overview
├── App.tsx              # Main app component with routing
├── main.tsx             # Application entry point
├── index.css            # Global styles and Tailwind config
└── vite-env.d.ts        # TypeScript environment definitions
```

## 🎨 Customization

### Replacing the Logo Animation

1. Create or obtain a Lottie JSON animation file
2. Replace `/public/animations/logo.json` with your animation
3. Ensure the animation dimensions work well with the responsive layout
4. Test on mobile devices and with reduced motion preferences

### Changing the Background Video

1. Add your video file to `/public/videos/`
2. Create poster images:
   - High-quality poster: `/public/images/poster.jpg`
   - Blurred placeholder: `/public/images/poster-blur.jpg`
3. Update the `LandingHero` component props:

```tsx
<LandingHero
  videoSrc="/videos/your-video.mp4"
  posterSrc="/images/your-poster.jpg"
  blurredPosterSrc="/images/your-poster-blur.jpg"
/>
```

### Customizing Styles

The project uses Tailwind CSS with custom color schemes:

```css
/* Custom color palette in tailwind.config.js */
colors: {
  ocean: { /* Ocean blue variants */ },
  deep: { /* Dark theme variants */ }
}
```

## 🧪 Testing

### Unit Tests
```bash
# Run unit tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests in watch mode
npm run test:watch
```

### End-to-End Tests
```bash
# Install Playwright browsers
npx playwright install

# Run E2E tests
npm run test:e2e
```

### Type Checking
```bash
# Run TypeScript type checking
npm run type-check
```

## 📦 Build & Deployment

### Development Build
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

### Production Deployment

The application builds to static files and can be deployed to any static hosting service:

- **Vercel**: Connect your repository for automatic deployments
- **Netlify**: Drag and drop the `dist` folder or connect via Git
- **AWS S3**: Upload the `dist` folder to an S3 bucket
- **Docker**: Use the included Dockerfile for containerized deployment

#### Environment Variables for Production

Ensure these environment variables are set in your production environment:

```env
VITE_API_BASE=https://your-api-domain.com
VITE_ENV=production
```

## 🔌 API Integration

The frontend integrates with the FastAPI backend using these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/floats` | List all floats with optional filters |
| GET | `/floats/{id}` | Get specific float information |
| GET | `/floats/{id}/details` | Get detailed float data with profiles |
| GET | `/floats/{id}/profiles` | Get float profile data |
| GET | `/floats/{id}/temperature-series` | Get temperature time series |
| POST | `/floats/{id}/click` | Log float interaction |
| GET | `/stats` | Get system statistics |
| GET | `/profiles/latest` | Get latest profiles for all floats |
| GET | `/export/{format}` | Export data in various formats |

### API Client Features

- **Automatic Retry**: Configurable retry logic with exponential backoff
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Type Safety**: Full TypeScript support with generated types
- **Response Caching**: React Query integration for optimal performance
- **Request Logging**: Detailed logging for debugging

## 🎯 Performance Optimization

### Bundle Size Optimization
- **Code Splitting**: Routes are lazy-loaded
- **Tree Shaking**: Unused code is automatically removed
- **Asset Optimization**: Images and videos are optimized
- **Chunk Strategy**: Vendor libraries are separated into chunks

### Runtime Performance
- **React Query**: Intelligent caching and background updates
- **Memoization**: Strategic use of React.memo and useMemo
- **Virtual Scrolling**: For large datasets (when implemented)
- **Image Lazy Loading**: Progressive image loading

### Accessibility
- **WCAG 2.1**: Follows Web Content Accessibility Guidelines
- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: ARIA labels and semantic HTML
- **Color Contrast**: High contrast ratios for readability
- **Motion Preferences**: Respects reduced motion settings

## 🐛 Troubleshooting

### Common Issues

#### API Connection Issues
```bash
# Check if the API server is running
curl http://127.0.0.1:8061/health

# Verify environment variables
echo $VITE_API_BASE
```

#### Build Issues
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf dist .vite
npm run build
```

#### TypeScript Errors
```bash
# Run type checking
npm run type-check

# Update TypeScript and related packages
npm update typescript @types/react @types/react-dom
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style and conventions
- Write unit tests for new components
- Update documentation for API changes
- Test accessibility features
- Optimize for performance

## 📄 License

This project is part of the NITW SIH (Smart India Hackathon) submission for oceanographic data visualization.

## 👥 Team

- **Anuprabh** - Backend Development
- **Aaron** - Frontend Development & Integration  
- **Manvitha** - UI/UX Design
- **Shreeya** - Data Analysis
- **Ashish** - System Architecture
- **Disha** - Testing & Quality Assurance

---

**Built with ❤️ for ocean research and data visualization**
