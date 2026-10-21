# Safe Files to Delete - Free Up 83+ GB

## BIGGEST: Downloads Folder - 79.32 GB 🎯

Your Downloads folder has **79 GB** of files!

### Quick Delete (Safe)
```powershell
# View what's in Downloads first
Get-ChildItem C:\Users\my277\Downloads | Sort-Object Length -Descending | Select-Object Name, @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB, 2)}} -First 20

# Delete everything (CAREFUL - review first!)
Remove-Item C:\Users\my277\Downloads\* -Recurse -Force
```

**OR** manually go to Downloads folder and delete:
- Old installers (`.exe`, `.msi`)
- Zip files
- Old downloads you don't need

---

## SECOND: AppData Folder - 49.23 GB

Contains caches and temp data.

### Safe to Delete:
```powershell
# 1. Temp folder - 0.71 GB
Remove-Item $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue

# 2. npm cache - 2.57 GB
Remove-Item C:\Users\my277\AppData\Local\npm-cache -Recurse -Force -ErrorAction SilentlyContinue

# 3. Python cache
Remove-Item C:\Users\my277\AppData\Local\pip -Recurse -Force -ErrorAction SilentlyContinue

# 4. Browser caches (Chrome, Edge, Firefox)
Remove-Item "C:\Users\my277\AppData\Local\Google\Chrome\User Data\Default\Cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\my277\AppData\Local\Microsoft\Edge\User Data\Default\Cache" -Recurse -Force -ErrorAction SilentlyContinue
```

---

## THIRD: Videos - 2.88 GB

Move or delete old videos you don't need.

---

## Quick Command to Free 80+ GB

**CAREFUL - This deletes Downloads folder! Review first!**

```powershell
# Step 1: View Downloads first
explorer C:\Users\my277\Downloads

# Step 2: After reviewing, delete
Remove-Item C:\Users\my277\Downloads\* -Recurse -Force

# Step 3: Clear caches
Remove-Item $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item C:\Users\my277\AppData\Local\npm-cache -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item C:\Users\my277\.cache\* -Recurse -Force -ErrorAction SilentlyContinue

# Step 4: Empty Recycle Bin
Clear-RecycleBin -Force
```

---

## Safe One-Line Command (Conservative - 3 GB)

This only deletes temp files and caches (safe):

```powershell
Remove-Item $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item C:\Users\my277\AppData\Local\npm-cache -Recurse -Force -ErrorAction SilentlyContinue; Clear-RecycleBin -Force -ErrorAction SilentlyContinue
```

---

## After Freeing Space

```powershell
# Check available space
Get-PSDrive C

# Install Next.js
cd C:\Users\my277\ntra\prospector-ai\web
npm install
npm run dev
```

---

## Summary

| Location | Size | Safe to Delete? |
|----------|------|-----------------|
| **Downloads** | 79.32 GB | ✅ YES (review first) |
| **AppData** | 49.23 GB | ⚠️ Partial (caches only) |
| **Temp files** | 0.71 GB | ✅ YES |
| **npm cache** | 2.57 GB | ✅ YES |
| **Videos** | 2.88 GB | ⚠️ Maybe (if not needed) |
| **.cache** | 0.67 GB | ✅ YES |

**Total recoverable: 83+ GB**

---

## Recommendation

1. **Open Downloads folder** and delete what you don't need (could free 79 GB!)
2. **Run the safe command** to clear caches (3 GB)
3. **Empty Recycle Bin**
4. Then install Next.js

You only need 500 MB free, so even deleting a few GB from Downloads will work!
