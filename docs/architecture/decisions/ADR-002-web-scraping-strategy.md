# ADR-002: Web Scraping Strategy

**Status:** Accepted

**Date:** 2025-11-18

**Context:**

DevMatch needs to extract job descriptions from job posting URLs. The ideal solution would be a unified API across all job platforms, but the reality is:

1. **Most job sites don't offer public APIs**: LinkedIn, Indeed, Glassdoor, and others provide APIs only to official partners or charge for access.

2. **Job boards use different technologies**: Some are server-rendered HTML (easy to scrape), others are JavaScript SPAs requiring browser rendering.

3. **Anti-scraping measures**: Many sites actively block scrapers using rate limiting, CAPTCHAs, and bot detection.

4. **Structure variability**: Each site uses different HTML structure, class names, and data formats.

5. **Terms of Service**: Web scraping may violate ToS, creating legal/ethical considerations.

6. **Reliability requirements**: For DevMatch to be useful, job scraping must work consistently across platforms.

**Decision:**

We will implement a **multi-strategy scraping approach** with these components:

1. **Direct JD Paste (Primary)**: Allow users to paste job description text directly, bypassing scraping entirely. This will be the recommended input method.

2. **Platform-Specific Scrapers**: Build custom scrapers for high-priority platforms:
   - **Indeed**: HTTP + BeautifulSoup (server-rendered)
   - **Google Jobs**: Structured data extraction
   - **LinkedIn**: Playwright + Chromium (JavaScript-rendered)

3. **Generic Fallback**: Best-effort extraction for unknown URLs using Playwright with heuristic content detection.

4. **Graceful Degradation**: If scraping fails, return partial data or prompt user to use direct paste.

**Rationale:**

1. **Direct Paste Solves Core Problem**: The scraping problem is a convenience feature, not core to the value proposition. Users can always copy-paste job descriptions.

2. **Platform Prioritization**: Indeed and Google Jobs are high-volume, scrapeable platforms. LinkedIn is valuable but fragile, so we implement it but don't depend on it.

3. **Multiple Tools for Different Sites**:
   - **BeautifulSoup**: Fast, lightweight for simple HTML. Works for Indeed.
   - **Playwright**: Handles JavaScript rendering. Required for LinkedIn, useful as fallback.

4. **User Control**: Letting users paste text gives them control and works for any site, including those with anti-bot measures.

5. **Ethical Considerations**: Scraping for individual job seeker use (not mass data collection) falls into a gray area. Providing direct paste as the primary method reduces ethical concerns.

**Technical Implementation:**

```python
class JobScraperService:
    def scrape_job(self, url: str = None, text: str = None):
        # Priority 1: Direct text paste
        if text:
            return self.parse_job_text(text)

        # Priority 2: Platform-specific scraper
        platform = self.detect_platform(url)
        if platform == "indeed":
            return self.scrape_indeed(url)
        elif platform == "google_jobs":
            return self.scrape_google_jobs(url)
        elif platform == "linkedin":
            return self.scrape_linkedin(url)

        # Priority 3: Generic fallback
        return self.scrape_generic(url)
```

**Scraping Strategies by Platform:**

| Platform | Method | Selectors | Reliability |
|----------|--------|-----------|-------------|
| **Indeed** | BeautifulSoup | `h1.jobsearch-JobInfoHeader-title`, `div#jobDescriptionText` | High |
| **Google Jobs** | Structured data | JSON-LD schema | High |
| **LinkedIn** | Playwright | `.top-card-layout__title`, `.description__text` | Medium |
| **Generic** | Playwright | Heuristic (largest text block) | Low |
| **Direct Paste** | User input | N/A | Very High |

**Consequences:**

**Positive:**
- Users can always use the service (direct paste never fails)
- Platform-specific scrapers work well for supported sites
- Playwright fallback handles edge cases
- No dependence on external APIs
- Zero cost (no API fees)

**Negative:**
- Scrapers are fragile (sites change HTML structure)
- Playwright requires browser binary (increases Docker image size)
- Anti-bot measures may block requests
- Ethical/legal gray area
- Maintenance burden (updating selectors when sites change)

**Mitigation Strategies:**

1. **Prominent Direct Paste Option**: Make text paste the primary, recommended method in the UI. Scraping is a convenience fallback.

2. **Graceful Failure**: If scraping fails, show friendly error and suggest direct paste. Never crash.

3. **Timeouts**: Hard 30-second timeout on scraping attempts to prevent hangs.

4. **User-Agent Rotation**: Use realistic browser user-agents to avoid simple bot detection.

5. **Retry Logic**: Single retry on timeout, then fail gracefully.

6. **Monitoring**: Log scraping success rates by platform to identify when selectors break.

**Alternatives Considered:**

1. **Third-Party Scraping APIs** (ScraperAPI, Bright Data): Reliable but costly ($30-100/month). Rejected due to cost for MVP.

2. **Official APIs Only**: Would limit to platforms with APIs (very few). Rejected as too restrictive.

3. **Scraping-Only (No Direct Paste)**: Would fail when scrapers break. Rejected as too fragile.

4. **Chrome Extension**: Would bypass scraping by running in user's browser. Rejected due to distribution complexity and limited mobile support.

**Legal/Ethical Considerations:**

- **Robots.txt**: We will respect robots.txt where feasible
- **Rate Limiting**: No aggressive scraping, single request per user action
- **Use Case**: Individual job seekers, not data harvesting
- **ToS Risk**: Acknowledged. Direct paste option mitigates by putting choice in user's hands
- **No CAPTCHA Solving**: We will not implement CAPTCHA solving (clear ethical line)

**Review Triggers:**

Re-evaluate this decision when:
- Scraping success rate drops below 70% on any supported platform
- We receive cease-and-desist notices
- Third-party APIs become affordable (<$10/month)
- User feedback indicates scraping is causing problems

**Notes:**

This decision prioritizes pragmatism and user value over technical purity. Direct paste ensures the core functionality always works, while scraping provides convenience when possible. The multi-strategy approach balances reliability with user experience.
