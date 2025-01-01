 # Application Icon Guide

## Icon Requirements
- Recommended sizes:
  - 16x16 pixels (small icon)
  - 32x32 pixels (standard icon)
  - 48x48 pixels (large icon)
  - 256x256 pixels (high-resolution)

## Platform-Specific Icon Formats
- Windows: `.ico`
- macOS: `.icns`
- Linux: `.png`

## Creating Icons

### Tools
- Adobe Photoshop
- GIMP (Free)
- Inkscape (Vector-based)
- Online Icon Generators

### Conversion Process
```bash
# Convert PNG to ICO (Windows)
convert input.png -resize 256x256 app_icon.ico

# Convert to ICNS (macOS)
# Using iconutil (macOS)
mkdir app_icon.iconset
sips -z 16 16   input.png --out app_icon.iconset/icon_16x16.png
sips -z 32 32   input.png --out app_icon.iconset/icon_16x16@2x.png
# ... (repeat for various sizes)
iconutil -c icns app_icon.iconset
Icon Placement
Copyresources/
└── icons/
    ├── app_icon.png     # Universal PNG
    ├── app_icon.ico     # Windows icon
    └── app_icon.icns    # macOS icon
Setting Icon in PyQt6
pythonCopyfrom PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

# In main application
app = QApplication(sys.argv)
app_icon = QIcon('resources/icons/app_icon.png')
app.setWindowIcon(app_icon)

# For specific window
main_window = QMainWindow()
main_window.setWindowIcon(app_icon)
Packaging Considerations

Include icon in PyInstaller spec file
Ensure icon is copied to distribution

pythonCopy# PyInstaller example
pyinstaller --icon=resources/icons/app_icon.ico main.py
Best Practices

Use simple, recognizable design
Ensure good visibility at small sizes
Use transparent background
Maintain brand consistency

