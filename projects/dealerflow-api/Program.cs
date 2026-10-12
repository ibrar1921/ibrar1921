using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<DealerDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("Dealers") ?? "Data Source=dealerflow.db"));
var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<DealerDbContext>();
    await db.Database.EnsureCreatedAsync();
}
app.MapGet("/health", () => Results.Ok(new { status = "ok", service = "dealerflow-api" }));

app.MapGet("/api/dealers", async (DealerDbContext db) =>
    Results.Ok(await db.Dealers.AsNoTracking().OrderBy(d => d.Name)
        .Select(d => new { d.Id, d.Name, d.Region, d.CreatedAt }).ToListAsync()));

app.MapGet("/api/dealers/{id:guid}", async (Guid id, DealerDbContext db) =>
{
    var dealer = await db.Dealers.AsNoTracking().Where(d => d.Id == id)
        .Select(d => new { d.Id, d.Name, d.Region, d.CreatedAt }).FirstOrDefaultAsync();
    return dealer is null ? Results.NotFound() : Results.Ok(dealer);
});

app.MapPost("/api/dealers", async (DealerInput input, DealerDbContext db) =>
{
    if (string.IsNullOrWhiteSpace(input.Name) || input.Name.Length > 120 ||
        string.IsNullOrWhiteSpace(input.Region) || input.Region.Length > 80)
        return Results.BadRequest(new { error = "Valid name (<=120) and region (<=80) required" });
    var dealer = new Dealer { Name = input.Name.Trim(), Region = input.Region.Trim() };
    db.Dealers.Add(dealer);
    await db.SaveChangesAsync();
    return Results.Created($"/api/dealers/{dealer.Id}", new { dealer.Id, dealer.Name, dealer.Region });
});

app.MapGet("/api/listings", async (string? status, Guid? dealerId, DealerDbContext db) =>
{
    var query = db.Listings.AsNoTracking().AsQueryable();
    if (!string.IsNullOrWhiteSpace(status)) query = query.Where(l => l.Status == status.ToLower());
    if (dealerId is not null) query = query.Where(l => l.DealerId == dealerId);
    return Results.Ok(await query.OrderByDescending(l => l.CreatedAt)
        .Select(l => new { l.Id, l.DealerId, l.Title, l.Price, l.Status, l.CreatedAt }).ToListAsync());
});

app.MapPost("/api/listings", async (ListingInput input, DealerDbContext db) =>
{
    if (input.DealerId == Guid.Empty || string.IsNullOrWhiteSpace(input.Title) ||
        input.Title.Length > 180 || input.Price <= 0 || input.Price > 1_000_000_000m)
        return Results.BadRequest(new { error = "Valid dealer, title (<=180) and positive price required" });
    if (!await db.Dealers.AnyAsync(d => d.Id == input.DealerId))
        return Results.NotFound(new { error = "Dealer does not exist" });
    var listing = new Listing { DealerId = input.DealerId, Title = input.Title.Trim(), Price = input.Price };
    db.Listings.Add(listing);
    await db.SaveChangesAsync();
    return Results.Created($"/api/listings/{listing.Id}", new {
        listing.Id, listing.DealerId, listing.Title, listing.Price, listing.Status });
});

app.MapGet("/api/listings/{id:guid}", async (Guid id, DealerDbContext db) =>
{
    var listing = await db.Listings.AsNoTracking().Where(l => l.Id == id)
        .Select(l => new { l.Id, l.DealerId, l.Title, l.Price, l.Status, l.CreatedAt })
        .FirstOrDefaultAsync();
    return listing is null ? Results.NotFound() : Results.Ok(listing);
});

app.MapPatch("/api/listings/{id:guid}/status", async (Guid id, StatusInput input, DealerDbContext db) =>
{
    var listing = await db.Listings.FindAsync(id);
    if (listing is null) return Results.NotFound();
    var requested = input.Status?.Trim().ToLowerInvariant() ?? "";
    var allowed = listing.Status switch
    {
        "draft" => new[] { "published", "closed" },
        "published" => new[] { "closed" },
        _ => Array.Empty<string>()
    };
    if (!allowed.Contains(requested))
        return Results.BadRequest(new { error = $"Cannot change {listing.Status} to {requested}" });
    listing.Status = requested;
    await db.SaveChangesAsync();
    return Results.Ok(new { listing.Id, listing.Status });
});
app.Run();
public partial class Program { }
