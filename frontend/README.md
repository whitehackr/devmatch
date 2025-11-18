# DevMatch Frontend

React frontend for DevMatch - GitHub Skills to Job Matcher

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client

## Features

- Mobile-first responsive design
- Direct job description paste (recommended)
- Job URL scraping support (Indeed, Google Jobs, LinkedIn)
- Real-time loading states with progress indicators
- Detailed match results with visualizations
- Skills breakdown (matched vs missing)
- GitHub profile summary
- Actionable recommendations

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── components/   # React components
│   │   ├── Header.jsx
│   │   ├── InputForm.jsx
│   │   ├── LoadingState.jsx
│   │   ├── Results.jsx
│   │   ├── ScoreCard.jsx
│   │   ├── RecommendationCard.jsx
│   │   ├── SkillsBreakdown.jsx
│   │   ├── GitHubProfileSummary.jsx
│   │   └── JobDetailsSummary.jsx
│   ├── services/     # API client
│   │   └── api.js
│   ├── App.jsx       # Main component
│   ├── main.jsx      # Entry point
│   └── index.css     # Global styles
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Component Overview

### InputForm
- Job URL or direct paste input
- GitHub username input
- Form validation
- Error handling

### LoadingState
- Animated spinner
- Progress messages
- Step-by-step indicators

### Results
- Orchestrates result display
- Manages "New Analysis" flow

### ScoreCard
- Overall, Required, Preferred scores
- Color-coded (green/yellow/red)
- Visual percentage displays

### RecommendationCard
- APPLY_NOW / COMPETITIVE / SKILL_GAP
- Gap analysis metrics
- Learning time estimates

### SkillsBreakdown
- Matched skills with evidence
- Missing skills by importance
- Category badges

### GitHubProfileSummary
- Language percentages with bars
- Framework and tool lists
- Account age and activity

### JobDetailsSummary
- Job title and company
- Required vs preferred skills
- Importance ratings

## Design System

### Colors
- Primary: `#2563EB` (Blue)
- Success: `#10B981` (Green)
- Warning: `#F59E0B` (Yellow)
- Danger: `#EF4444` (Red)

### Typography
- System font stack for performance
- Tailwind's default scale

### Spacing
- 8px grid system (Tailwind default)

### Responsive Breakpoints
- Mobile: < 768px
- Desktop: >= 768px

## API Integration

See `src/services/api.js` for API client configuration.

Endpoints used:
- `POST /api/analyze` - Main analysis endpoint
- `GET /health` - Health check

## Deployment

See [../docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) for deployment instructions.

### Vercel Deployment

1. Connect GitHub repository
2. Set build settings:
   - Framework: Vite
   - Build command: `npm run build`
   - Output directory: `dist`
3. Set environment variable:
   - `VITE_API_URL`: Your Railway backend URL
4. Deploy!

## License

MIT
