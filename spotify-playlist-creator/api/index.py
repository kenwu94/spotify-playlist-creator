import sys
import os

# Debug information
print(f"🔍 Current file: {__file__}")
print(f"📁 Current directory: {os.path.dirname(__file__)}")

# Add the src directory to the Python path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
src_path = os.path.abspath(src_path)
print(f"📂 Src path: {src_path}")
print(f"✅ Src path exists: {os.path.exists(src_path)}")

sys.path.insert(0, src_path)

# Check if main.py exists
main_path = os.path.join(src_path, 'main.py')
print(f"📄 Main.py path: {main_path}")
print(f"✅ Main.py exists: {os.path.exists(main_path)}")

# Now try to import
try:
    from main import app
    print("✅ Import successful!")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    raise

# Export for Vercel (Vercel looks for 'app' at module level)
# Don't reassign the app variable, just make it available
application = app

# For local testing
if __name__ == "__main__":
    print("🎵 Starting app from API entry point...")
    app.run(debug=True, host='0.0.0.0', port=5000)