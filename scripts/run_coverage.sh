#!/bin/bash
# Script pentru rulare teste cu coverage report
# Generează raport HTML în htmlcov/

echo "🧪 Running tests with coverage..."
echo "=================================="

# Rulează pytest cu coverage
pytest --cov=. --cov-report=html --cov-report=term \
    --cov-config=.coveragerc \
    -v

# Verifică exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Tests completed successfully!"
    echo "📊 Coverage report generated in htmlcov/index.html"
    echo ""
    echo "To view the report, open: htmlcov/index.html"
else
    echo ""
    echo "❌ Some tests failed. Check the output above."
    exit 1
fi
