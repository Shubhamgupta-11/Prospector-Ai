# Next.js Frontend Setup Instructions

## Step 1: Initialize Next.js Project

```bash
cd c:\Users\my277\ntra\prospector-ai
npx create-next-app@latest web --typescript --tailwind --app --no-src-dir --import-alias "@/*"
```

When prompted, select:
- ✅ TypeScript
- ✅ ESLint  
- ✅ Tailwind CSS
- ✅ App Router
- ❌ src/ directory
- ✅ Import alias (@/*)

## Step 2: Install shadcn/ui

```bash
cd web
npx shadcn@latest init
```

When prompted, select:
- Style: **New York**
- Base color: **Slate**
- CSS variables: **Yes**

## Step 3: Install Required shadcn Components

```bash
npx shadcn@latest add card button input tabs progress badge
```

## Step 4: Install Additional Dependencies

```bash
npm install lucide-react clsx tailwind-merge
```

## Step 5: Start Development Server

```bash
npm run dev
```

Frontend will be available at: **http://localhost:3000**

## Step 6: Update Backend CORS (if needed)

Make sure your FastAPI backend allows requests from localhost:3000.

---

That's it! The Next.js frontend is ready to use.
