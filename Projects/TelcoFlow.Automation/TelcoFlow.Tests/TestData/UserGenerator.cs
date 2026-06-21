using Bogus;

namespace TelcoFlow.Tests.TestData
{
    public class TelecomUser
    {
        public string FullName { get; set; } = string.Empty;
public string PhoneNumber { get; set; } = string.Empty;
public string Email { get; set; } = string.Empty;
        public decimal AccountBalance { get; set; }
    }

    public static class UserGenerator
    {
        public static TelecomUser GenerateValidUser()
        {
            var faker = new Faker<TelecomUser>()
                .RuleFor(u => u.FullName, f => f.Name.FullName())
                .RuleFor(u => u.PhoneNumber, f => f.Phone.PhoneNumber("+9955#########"))
                .RuleFor(u => u.Email, f => f.Internet.Email())
                .RuleFor(u => u.AccountBalance, f => f.Random.Decimal(5, 100));

            return faker.Generate();
        }
    }
}