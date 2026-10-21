# Commands to Initialize and Run the Web Frontend

## Step 1: Install Node.js Dependencies

```bash
cd web
npm install
```

This will install all required packages:
- Next.js 15
- React 18
- Tailwind CSS
- shadcn/ui components (Radix UI primitives)
- Lucide React icons
- TypeScript

## Step 2: Start the Development Server

```bash
npm run dev
```

Or from the root directory:
```bash
cd c:\Users\my277\ntra\prospector-ai
.\start_web.bat
```

## Step 3: Open in Browser

Navigate to: **http://localhost:3000**

---

## What's Built

### Pages
- **Homepage** (`/`) - Search interface with centered input
- **Results Dashboard** - Displays research data with tabs

### Components
- Clean dark mode UI
- shadcn/ui components (Button, Card, Input, Badge, Progress, Tabs)
- Enterprise-grade minimalist design
- NO emojis (as requested)

### Features
- Real-time research fetching from FastAPI backend
- Loading states with animations
- Intent score visualization with progress bars
- Gap analysis display
- Outreach message generation with copy-to-clipboard
- Source citations with external links
- Responsive design

---

## Backend Integration

The frontend expects the FastAPI backend to be running at:
```
http://localhost:8000
```

API Endpoint used:
```
POST /api/v1/research
```

Make sure your backend has CORS enabled for `localhost:3000`.

---

## Project Structure

```
web/
├── app/
│   ├── layout.tsx          # Root layout with dark mode
│   ├── page.tsx            # Main page component
│   └── globals.css         # Tailwind + shadcn styles
├── components/
│   └── ui/                 # shadcn components
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── badge.tsx
│       ├── progress.tsx
│       └── tabs.tsx
├── lib/
│   └── utils.ts            # Utility functions (cn helper)
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.ts
```

---

## Design System

### Colors
- Dark background with slate tones
- Primary: Blue (#3B82F6)
- Borders: Subtle grays
- Text: High contrast white/gray

### Typography
- Font: Inter (system font)
- Sizes: Professional scale
- Weight: Semibold for headers

### Components
- Rounded corners (0.5rem)
- Subtle shadows
- Clean borders
- Minimal padding

### No Emojis
As requested, the UI uses ZERO emojis. Icons from Lucide React instead.

---

## Build for Production

```bash
npm run build
npm start
```

---

## Troubleshooting

### Port 3000 already in use
```bash
# Kill the process or use different port
npm run dev -- -p 3001
```

### Backend not responding
- Ensure FastAPI is running on port 8000
- Check CORS settings in FastAPI
- Verify API endpoint: http://localhost:8000/api/v1/research

### TypeScript errors
```bash
npm run lint
```

---

You're ready to showcase! 🚀
