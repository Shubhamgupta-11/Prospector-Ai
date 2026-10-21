# DISK SPACE ISSUE - Action Required

## Problem

Your C: drive has **0 bytes free**. Node.js package installation requires significant disk space (typically 200-500MB for node_modules).

## Immediate Actions

### Option 1: Free Up Space on C: Drive

1. **Delete Temporary Files**
   ```powershell
   # Run Disk Cleanup
   cleanmgr /d C:
   ```

2. **Clear npm cache** (after freeing space)
   ```powershell
   npm cache clean --force
   ```

3. **Delete large files/folders:**
   - Downloads folder
   - Temp files (%TEMP%)
   - Old Windows updates
   - Recycle Bin

4. **Use Windows Storage Settings:**
   - Settings > System > Storage
   - Click "Temporary files"
   - Delete unnecessary files

### Option 2: Use a Different Drive (Recommended)

If you have another drive with space (D:, E:, etc.):

```powershell
# Move the entire project to D: drive
cd \
xcopy /E /I c:\Users\my277\ntra\prospector-ai d:\prospector-ai

# Then work from D:
cd d:\prospector-ai\web
npm install
npm run dev
```

### Option 3: Simplified Frontend (No Node Modules)

I can create a simple standalone HTML file that doesn't require npm/node_modules:

```html
<!-- Single HTML file with inline JS and Tailwind CDN -->
<!-- No build process needed -->
<!-- Can open directly in browser -->
```

Would you like me to create this simplified version?

---

## How Much Space Needed

- **node_modules**: ~300-400 MB
- **Next.js build**: ~50-100 MB
- **Total recommended**: 500 MB+ free space

---

## Current Situation

Your C: drive shows:
- Used: 332 GB
- Free: 0 GB

**You need to free up at least 500 MB to proceed.**

---

## Quick Commands to Check Space

```powershell
# Check all drives
Get-PSDrive -PSProvider FileSystem

# Find largest folders
Get-ChildItem C:\ -Directory | 
  ForEach-Object { 
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | 
      Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{
      Folder = $_.Name
      SizeGB = [math]::Round($size/1GB, 2)
    }
  } | Sort-Object SizeGB -Descending
```

---

## Next Steps

1. Choose an option above
2. Free up space or move to another drive
3. Run: `cd web && npm install`
4. Start the frontend: `npm run dev`

Let me know which option you'd prefer!
