# ADR-001: Stateless Architecture

**Status:** Accepted

**Date:** 2025-11-18

**Context:**

When building DevMatch, we faced a fundamental architectural decision: should the system maintain state (user sessions, cached results, request history) or operate statelessly where each request is independent?

Several forces are at play:

1. **Operational Complexity**: Databases require setup, maintenance, backups, and monitoring. For an MVP, this adds significant overhead.

2. **Scalability**: Stateless services scale horizontally trivially - just add more instances. Stateful services require session affinity, distributed caching, or database sharding.

3. **Development Speed**: Building without a database means no schema migrations, no ORM configuration, no data modeling debates. This accelerates iteration.

4. **Cost**: Managed databases cost money. Free tiers exist but have limitations. Zero database = zero database costs.

5. **User Experience Trade-offs**: Without persistence, users cannot save results or track history. However, the core value proposition (getting a match score) doesn't inherently require persistence.

6. **Caching Benefits**: GitHub profiles and job descriptions change slowly. Caching could reduce API calls and improve response times. However, cache invalidation is complex and cache hits may be low for an early-stage product.

**Decision:**

We will build DevMatch as a **stateless application** with no database. Each API request will:
- Fetch all required data fresh (job description, GitHub profile)
- Perform analysis in-memory
- Return complete results
- Retain no state after response

**Rationale:**

1. **MVP Focus**: The goal is to validate the core concept (GitHub-based matching). Persistence is not essential for this validation.

2. **Operational Simplicity**: Deploying a single containerized service is dramatically simpler than coordinating backend + database + migrations.

3. **Cost Efficiency**: Free hosting tiers (Railway, Vercel) work perfectly for stateless apps. Database hosting would require paid plans or management overhead.

4. **Development Velocity**: Building stateless means we can iterate on the matching algorithm, NLP extraction, and UI without worrying about data migrations or backwards compatibility.

5. **Real-time Data**: Analyzing GitHub profiles fresh each time ensures results reflect the user's most recent work. Cached results could be stale.

6. **Horizontal Scalability**: If the service gains traction, scaling is trivial: deploy more backend instances behind a load balancer.

**Consequences:**

**Positive:**
- Faster MVP delivery (no database setup, no schema design)
- Simpler deployment (single service)
- Zero database costs
- Trivial horizontal scaling
- No data migration concerns
- Always-fresh results (no stale cache issues)

**Negative:**
- Cannot store user history (past analyses, tracked jobs)
- No caching of expensive operations (GitHub API calls, job scraping)
- Repeat users re-fetch same data
- Higher GitHub API usage (could hit rate limits)
- Cannot implement features requiring persistence (job alerts, application tracking)

**Mitigation Strategies:**

1. **Rate Limiting**: GitHub API limits (60 req/hour unauthenticated) are acceptable for MVP traffic. If needed, users can provide Personal Access Tokens for 5000 req/hour.

2. **Future State Layer**: If the product validates, we can add a caching layer (Redis) or database (PostgreSQL) without changing the core architecture. The stateless services become the "business logic layer" with a separate "data layer" added on top.

3. **Client-Side Caching**: The frontend can store previous results in browser localStorage, giving returning users a "history" without backend state.

4. **Progressive Enhancement**: Core flow works statelessly. Advanced features (history, alerts) can be added later as paid features that justify infrastructure costs.

**Alternatives Considered:**

1. **PostgreSQL Database**: Full persistence with user accounts, history, and caching. Rejected due to complexity and cost for unvalidated MVP.

2. **Redis Caching Layer**: In-memory cache for GitHub profiles and job descriptions. Rejected because cache invalidation is complex and hit rates would be low initially.

3. **Hybrid Approach**: Stateless core with optional user accounts. Rejected as premature optimization before understanding actual user needs.

**Review Triggers:**

Re-evaluate this decision when:
- Monthly active users exceed 1,000 (rate limiting becomes issue)
- Users explicitly request history/tracking features
- GitHub API rate limits cause degraded experience
- Response times exceed 60 seconds due to repeated fetching

**Notes:**

This decision reflects a deliberate choice to optimize for speed-to-market and learning over feature completeness. The architecture allows for adding state later without a complete rewrite, making this a low-risk, reversible decision.
