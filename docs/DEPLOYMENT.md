# DevMatch Deployment Guide

Complete guide for deploying DevMatch to production.

## Architecture

- **Backend**: Railway (containerized FastAPI app)
- **Frontend**: Vercel (static React SPA)
- **Database**: None (stateless architecture)

## Prerequisites

1. **GitHub Account** with repository access
2. **Railway Account** (free tier available)
3. **Vercel Account** (free tier available)
4. **GitHub Personal Access Token** (optional, for higher rate limits)

## Part 1: Backend Deployment (Railway)

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub account
3. Verify email

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select the `devmatch` repository
5. Railway will detect the Dockerfile

### Step 3: Configure Environment Variables

In Railway dashboard, add these environment variables:

| Variable | Value | Required | Description |
|----------|-------|----------|-------------|
| `PORT` | `8000` | Yes | Port for FastAPI (Railway sets this automatically) |
| `CORS_ORIGINS` | `https://your-vercel-app.vercel.app` | Yes | Frontend URL (update after Vercel deployment) |
| `GITHUB_TOKEN` | `ghp_xxxx...` | No | GitHub PAT for 5000 req/hour (recommended) |
| `ENVIRONMENT` | `production` | No | Environment name |

**Important**: You'll update `CORS_ORIGINS` after deploying the frontend.

### Step 4: Deploy

1. Railway will automatically build from Dockerfile
2. Build takes 5-10 minutes (installing dependencies, spaCy model, Playwright)
3. Once deployed, Railway provides a public URL: `https://your-app.up.railway.app`
4. **Save this URL** - you'll need it for frontend

### Step 5: Verify Deployment

Test the health endpoint:

```bash
curl https://your-app.up.railway.app/health
```

Should return:
```json
{"status": "healthy", "version": "1.0.0"}
```

### Step 6: Configure Custom Domain (Optional)

1. In Railway dashboard, go to Settings → Domains
2. Click "Generate Domain" or "Add Custom Domain"
3. Follow instructions for DNS configuration

## Part 2: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub account

### Step 2: Import Project

1. Click "New Project"
2. Import the `devmatch` repository
3. Vercel will detect it's a monorepo

### Step 3: Configure Project Settings

**Root Directory**: `frontend`

**Framework Preset**: Vite

**Build & Output Settings**:
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

### Step 4: Environment Variables

Add this environment variable:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://your-app.up.railway.app` |

Use the Railway URL from Part 1, Step 4.

### Step 5: Deploy

1. Click "Deploy"
2. Vercel will build and deploy (2-3 minutes)
3. You'll get a URL: `https://devmatch.vercel.app` (or custom)

### Step 6: Update Backend CORS

1. Go back to Railway dashboard
2. Update `CORS_ORIGINS` environment variable to your Vercel URL
3. Railway will automatically redeploy

## Part 3: GitHub Personal Access Token (Optional but Recommended)

### Why?

- GitHub API has a 60 requests/hour limit for unauthenticated requests
- A Personal Access Token increases this to 5,000 requests/hour
- DevMatch uses ~50-70 requests per analysis

### How to Create

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name: "DevMatch API"
4. Expiration: Choose duration (90 days recommended)
5. Scopes: **No scopes needed** (public data only)
6. Click "Generate token"
7. **Copy the token** (starts with `ghp_`)

### Add to Railway

1. Railway dashboard → Environment Variables
2. Add variable:
   - Name: `GITHUB_TOKEN`
   - Value: `ghp_your_token_here`
3. Save

## Part 4: Testing the Deployment

### Test 1: Health Check

```bash
curl https://your-backend-url/health
```

Expected: `{"status": "healthy", "version": "1.0.0"}`

### Test 2: Full Analysis

```bash
curl -X POST https://your-backend-url/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "We are seeking a Senior Python Engineer with Django and PostgreSQL experience. AWS knowledge is preferred.",
    "github_username": "gvanrossum"
  }'
```

Should return complete match result.

### Test 3: Frontend

1. Open `https://your-vercel-url` in browser
2. Enter a GitHub username: `torvalds`
3. Paste a job description
4. Click "Analyze Match"
5. Should see results in 30-60 seconds

## Part 5: Monitoring & Maintenance

### Railway Monitoring

**Metrics Available**:
- CPU usage
- Memory usage
- Request count
- Error rate
- Response time

**Logs**:
- View in Railway dashboard → Deployments → Logs
- Search and filter by timestamp

**Alerts** (Paid plan):
- Set up alerts for downtime
- Email/Slack notifications

### Vercel Monitoring

**Analytics**:
- Page views
- Unique visitors
- Performance metrics

**Deployment Logs**:
- Build logs
- Runtime logs (serverless functions)

### Common Issues

#### Issue 1: CORS Error in Frontend

**Symptom**: Browser console shows "CORS policy" error

**Solution**:
1. Check Railway `CORS_ORIGINS` includes your Vercel URL
2. Ensure URL has no trailing slash
3. Redeploy backend after updating

#### Issue 2: GitHub Rate Limit

**Symptom**: 403 errors, "API rate limit exceeded"

**Solution**: Add GitHub Personal Access Token (see Part 3)

#### Issue 3: Slow Analysis (>60 seconds)

**Symptom**: Timeout errors

**Possible Causes**:
- Large GitHub profiles (100+ repos)
- Slow network to GitHub API
- Cold start (Railway free tier)

**Solutions**:
- Use paid Railway plan (no cold starts)
- Reduce `MAX_REPOS_TO_ANALYZE` in config.py
- Optimize repository filtering

#### Issue 4: Scraping Fails

**Symptom**: "Failed to extract job description"

**Solution**: Use direct paste instead of URL (recommended)

## Part 6: Scaling & Optimization

### Current Limitations (Free Tier)

- **Railway Free Tier**:
  - $5 free credit/month
  - Sleeps after 15 minutes of inactivity
  - 512MB RAM
  - 1 vCPU
  - Shared network

- **Vercel Free Tier**:
  - 100GB bandwidth/month
  - Unlimited requests
  - Automatic scaling
  - Global CDN

### Scaling Recommendations

**When to upgrade**:
- 1000+ analyses/month → Railway Pro ($20/month)
- Need faster response times → Increase memory/CPU
- High traffic → Vercel Pro ($20/month) for analytics

**Optimization Options**:
1. **Caching**: Add Redis for GitHub profile caching
2. **Database**: PostgreSQL for user history
3. **Job Queue**: Celery + Redis for async processing
4. **CDN**: Cloudflare in front of Railway
5. **Monitoring**: Sentry for error tracking

## Part 7: Custom Domain Setup

### Railway Custom Domain

1. Railway dashboard → Settings → Domains
2. Click "Add Custom Domain"
3. Enter your domain: `api.devmatch.app`
4. Add CNAME record to your DNS:
   - Type: CNAME
   - Name: `api`
   - Value: `your-app.up.railway.app`
5. Wait for DNS propagation (5-60 minutes)

### Vercel Custom Domain

1. Vercel dashboard → Settings → Domains
2. Add domain: `devmatch.app`
3. Add DNS records (Vercel provides instructions)
4. Wait for verification

### Update CORS After Custom Domain

1. Update Railway `CORS_ORIGINS` to `https://devmatch.app`
2. Update Vercel `VITE_API_URL` to `https://api.devmatch.app`
3. Redeploy both

## Part 8: Rollback Procedure

### Railway Rollback

1. Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Redeploy"

### Vercel Rollback

1. Dashboard → Deployments
2. Find previous deployment
3. Click "..." → "Promote to Production"

## Part 9: Cost Estimates

### Free Tier (Recommended for MVP)

- Railway: $5 free credit/month (~500 analyses)
- Vercel: Free (100GB bandwidth, plenty for MVP)
- **Total**: $0/month

### Paid Tier (Production)

- Railway Pro: $20/month (no sleep, better performance)
- Vercel Pro: $20/month (analytics, team features)
- **Total**: $40/month

### API Costs

- GitHub API: Free (with PAT: 5000 req/hour)
- spaCy: Free (runs locally)
- No database costs (stateless)

## Part 10: Security Checklist

- [ ] HTTPS enabled (automatic on Railway/Vercel)
- [ ] CORS configured correctly
- [ ] GitHub token kept secret (environment variable)
- [ ] No sensitive data in logs
- [ ] Rate limiting implemented (future enhancement)
- [ ] Input validation in place (Pydantic)
- [ ] Dependencies up to date (`pip list --outdated`)

## Troubleshooting Commands

### Check Backend Logs

```bash
# Railway logs (via Railway CLI)
railway logs

# Or view in dashboard
```

### Check Frontend Build Logs

```bash
# View in Vercel dashboard → Deployments → Build Logs
```

### Test API Locally

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

### Verify Environment Variables

```bash
# Railway
railway variables

# Vercel (in project settings)
```

## Support

**Issues**: [GitHub Issues](https://github.com/your-username/devmatch/issues)

**Documentation**:
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)

---

**Deployment Checklist**:

- [ ] Railway account created
- [ ] Backend deployed on Railway
- [ ] Backend health check passes
- [ ] GitHub PAT configured (optional)
- [ ] Vercel account created
- [ ] Frontend deployed on Vercel
- [ ] CORS updated with Vercel URL
- [ ] End-to-end test completed
- [ ] Custom domains configured (optional)
- [ ] Monitoring set up

**Congratulations! Your DevMatch application is now live! 🎉**
