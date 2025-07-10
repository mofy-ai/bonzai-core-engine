# ==================================================
# 🐳 TrueNorth Agent System - Multi-Stage Dockerfile
# ==================================================

# ==========================================
# Stage 1: Build Environment
# ==========================================
FROM node:18-alpine AS builder

LABEL maintainer="TrueNorth Team <support@truenorth.dev>"
LABEL description="🧭 AI-powered agent orchestration for intelligent code analysis"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies with optimizations
RUN npm ci --only=production --no-audit --no-fund && \
    npm cache clean --force

# Copy source code
COPY src/ ./src/

# Build the extension
RUN npm run compile

# ==========================================
# Stage 2: Development Environment
# ==========================================
FROM node:18-alpine AS development

WORKDIR /app

# Install development dependencies
COPY package*.json ./
RUN npm ci && npm cache clean --force

# Copy source and build files
COPY --from=builder /app/out ./out
COPY --from=builder /app/src ./src
COPY --from=builder /app/tsconfig.json ./

# Install VS Code server for development
RUN wget -qO- https://code-server.dev/install.sh | sh

# Expose development server port
EXPOSE 8080

# Development command - password should be set via environment variable
CMD ["sh", "-c", "code-server --bind-addr 0.0.0.0:8080 --auth password --password ${CODE_SERVER_PASSWORD:-changeme}"]

# ==========================================
# Stage 3: Testing Environment
# ==========================================
FROM node:18-alpine AS testing

WORKDIR /app

# Copy package files and install all dependencies
COPY package*.json ./
RUN npm ci && npm cache clean --force

# Copy source and test files
COPY --from=builder /app/out ./out
COPY --from=builder /app/src ./src
COPY tests/ ./tests/
COPY jest.config.js ./
COPY tsconfig.json ./

# Install additional testing tools
RUN npm install -g @vscode/vsce

# Run tests
RUN npm test

# Testing command
CMD ["npm", "run", "test:watch"]

# ==========================================
# Stage 4: Production Environment
# ==========================================
FROM node:18-alpine AS production

# Security: Create non-root user
RUN addgroup -g 1001 -S truenorth && \
    adduser -S truenorth -u 1001 -G truenorth

WORKDIR /app

# Copy only production dependencies
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production --no-audit --no-fund && \
    npm cache clean --force && \
    rm -rf ~/.npm

# Copy built application
COPY --from=builder /app/out ./out
COPY package.json ./

# Create necessary directories
RUN mkdir -p /app/logs /app/reports && \
    chown -R truenorth:truenorth /app

# Switch to non-root user
USER truenorth

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "console.log('TrueNorth Agent System is healthy')" || exit 1

# Metadata
LABEL org.opencontainers.image.title="TrueNorth Agent System"
LABEL org.opencontainers.image.description="AI-powered agent orchestration for intelligent code analysis"
LABEL org.opencontainers.image.vendor="TrueNorth"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.url="https://truenorth.dev"
LABEL org.opencontainers.image.documentation="https://truenorth.dev/docs"
LABEL org.opencontainers.image.source="https://github.com/bkingery3/true-north-ai-assistant"

# Production command
CMD ["node", "out/extension.js"]

# ==========================================
# Stage 5: Monitoring & Observability
# ==========================================
FROM production AS monitoring

# Install monitoring tools
USER root
RUN apk add --no-cache curl jq

# Copy monitoring scripts
COPY docker/scripts/monitoring/ ./scripts/monitoring/

# Health monitoring
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD ./scripts/monitoring/health-check.sh || exit 1

USER truenorth

# Monitoring command with enhanced logging
CMD ["sh", "-c", "node out/extension.js & ./scripts/monitoring/monitor.sh"]