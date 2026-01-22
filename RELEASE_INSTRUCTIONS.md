# 🚀 Release Instructions

## How to Create a Release with Auto-Built Executables

This project uses GitHub Actions to automatically build executables for Windows, Linux, and macOS whenever you create a new release tag.

### Quick Start

**Option 1: Use the helper script (Recommended)**

Linux/Mac:
```bash
./create_release.sh
```

Windows:
```bash
create_release.bat
```

The script will:
1. Show you the current version
2. Ask for the new version (e.g., v1.0.0)
3. Create and push the git tag
4. Trigger GitHub Actions automatically

**Option 2: Manual tag creation**

```bash
# Create a tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Push the tag to GitHub
git push origin v1.0.0
```

### What Happens Next?

Once you push a version tag (format: `v*.*.*`), GitHub Actions will:

1. **Build Phase** (~5-10 minutes)
   - Checkout code on Windows, Linux, and macOS runners
   - Install Python and dependencies
   - Build standalone executables with PyInstaller
   - Upload artifacts

2. **Release Phase** (~1-2 minutes)
   - Download all built executables
   - Create a GitHub Release with the tag
   - Upload executables as release assets:
     - `MouseTracker-Windows.exe`
     - `MouseTracker-Linux`
     - `MouseTracker-macOS`
   - Generate release notes automatically

### Monitoring the Build

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Find the "Build Executables" workflow
4. Watch the progress in real-time

### After the Release

Once complete, users can:
1. Go to `https://github.com/YOUR_USERNAME/clod/releases`
2. Click on the latest release
3. Download the executable for their OS
4. Run it directly - no Python installation needed!

### Version Naming

Follow [Semantic Versioning](https://semver.org/):
- `v1.0.0` - Major version (breaking changes)
- `v1.1.0` - Minor version (new features)
- `v1.0.1` - Patch version (bug fixes)

### First Release

For your first release, we recommend starting with:
```bash
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0
```

This will trigger the build process and create your first downloadable release!

### Troubleshooting

**Build fails?**
- Check the Actions tab for error logs
- Ensure all tests pass locally first
- Verify `requirements.txt` is up to date

**Executables don't work?**
- Test locally with `python build_executable.py`
- Check PyInstaller compatibility with your dependencies
- Review the GitHub Actions logs

**Need to delete a release?**
```bash
# Delete remote tag
git push --delete origin v1.0.0

# Delete local tag
git tag -d v1.0.0

# Then delete the release on GitHub's web interface
```

### Testing Before Release

Before creating a release, test the build locally:
```bash
python build_executable.py
```

This ensures the executable builds successfully on your machine.

---

Ready to create your first release? Just run `./create_release.sh` and follow the prompts! 🎉
