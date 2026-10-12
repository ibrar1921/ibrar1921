# DealerFlow API 🏘️

A new **ASP.NET Core 8 + Entity Framework Core + SQLite** project inspired by dealer-management applications. This is **not** proprietary code from Ibrar's past Dealer's Net work.

### Functionality
- Persistent SQLite entities for dealers and their property listings.
- Dealer creation, read and list endpoints; listing creation, read and filter endpoints.
- Listing life cycle with validated `draft → published → closed` transitions.
- Input validation, structured responses and Docker container setup.

### Run
Install the .NET 8 SDK, then run:
```bash
dotnet restore
dotnet run --urls http://localhost:5070
curl http://localhost:5070/health
```

Alternatively build with `docker build -t dealerflow-api .` and run with `docker run --rm -p 8080:8080 dealerflow-api`.

1. Create a dealer: POST `/api/dealers` with a name and region.
2. Create a listing: POST `/api/listings` with dealer ID, title and positive price.
3. Query `GET /api/listings` or `GET /api/listings?status=published`.
4. Update status using PATCH `/api/listings/{id}/status`.

**Security & maturity:** Local development demonstration only, with **no authentication or authorization**. Do not expose to the public internet. `EnsureCreated` is intentionally used instead of production migrations. A .NET SDK was not available in the authoring environment; this code has **not yet been compiled**. Run `dotnet build` to validate on a machine with .NET 8 installed.
