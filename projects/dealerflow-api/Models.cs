using Microsoft.EntityFrameworkCore;

public sealed class Dealer
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Name { get; set; } = string.Empty;
    public string Region { get; set; } = string.Empty;
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
    public List<Listing> Listings { get; set; } = [];
}
public sealed class Listing
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid DealerId { get; set; }
    public Dealer Dealer { get; set; } = null!;
    public string Title { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Status { get; set; } = "draft";
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
}
public sealed class DealerDbContext(DbContextOptions<DealerDbContext> options) : DbContext(options)
{
    public DbSet<Dealer> Dealers => Set<Dealer>();
    public DbSet<Listing> Listings => Set<Listing>();
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Dealer>().HasIndex(d => d.Region);
        modelBuilder.Entity<Dealer>().Property(d => d.Name).HasMaxLength(120).IsRequired();
        modelBuilder.Entity<Listing>().HasIndex(l => new { l.DealerId, l.Status });
        modelBuilder.Entity<Listing>().Property(l => l.Title).HasMaxLength(180).IsRequired();
        modelBuilder.Entity<Listing>().HasOne(l => l.Dealer).WithMany(d => d.Listings)
            .HasForeignKey(l => l.DealerId).OnDelete(DeleteBehavior.Cascade);
    }
}
public record DealerInput(string Name, string Region);
public record ListingInput(Guid DealerId, string Title, decimal Price);
public record StatusInput(string Status);
