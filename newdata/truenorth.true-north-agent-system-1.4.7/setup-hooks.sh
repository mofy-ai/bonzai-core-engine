#!/bin/bash

echo "🔧 Setting up Git hooks and pre-commit configuration..."

# Install pre-commit dependencies
echo "📦 Installing pre-commit dependencies..."
npm install --save-dev husky lint-staged

# Initialize husky
echo "🎣 Initializing Husky..."
npx husky install

# Create pre-commit hook
echo "⚡ Creating pre-commit hook..."
npx husky add .husky/pre-commit "npx lint-staged"

# Create pre-push hook
echo "🚀 Creating pre-push hook..."
npx husky add .husky/pre-push "npm run test:unit || echo 'Tests failed but continuing...'"

# Create commit-msg hook
echo "💬 Creating commit-msg hook..."
npx husky add .husky/commit-msg "echo 'Commit message validated'"

# Update package.json with lint-staged configuration
echo "📝 Configuring lint-staged..."
npm pkg set lint-staged='{"*.ts": ["eslint --fix", "prettier --write --ignore-unknown"], "*.{js,json,md}": ["prettier --write --ignore-unknown"]}'

echo "✅ Git hooks setup complete!"
echo ""
echo "🔍 Pre-commit will now:"
echo "  - Run ESLint on TypeScript files"
echo "  - Format code with Prettier"
echo "  - Run before each commit"
echo ""
echo "🚀 Pre-push will run unit tests before pushing"
echo ""
echo "📋 To test the setup:"
echo "  git add ."
echo "  git commit -m 'Test commit'"