set -e

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔄 Applying migrations..."
python manage.py migrate

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "✅ Build completed!"