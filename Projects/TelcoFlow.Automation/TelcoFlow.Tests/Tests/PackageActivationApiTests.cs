using Xunit;
using FluentAssertions;
using TelcoFlow.Tests.Services;
using TelcoFlow.Tests.TestData;
using System.Net;
using System.Threading.Tasks;

namespace TelcoFlow.Tests.Tests
{
    public class PackageActivationApiTests
    {
        private readonly TelecomApiService _apiService;

        public PackageActivationApiTests()
        {
            _apiService = new TelecomApiService();
        }

        [Fact]
        public async Task ActivateRoaming_ShouldReturnSuccess_ForValidUser()
        {
            // Arrange: 1. ვაგენერირებთ დინამიურ ტელეკომის მომხმარებელს (Test Data Management)
            var testUser = UserGenerator.GenerateValidUser();
            var roamingPackageId = "ROAM_EU_10GB";

            // Act: 2. ვუშვებთ რეალურ API მოთხოვნას პაკეტის გასააქტიურებლად
            var response = await _apiService.ActivateRoamingPackageAsync(testUser.PhoneNumber, roamingPackageId);

            // Assert: 3. ვამოწმებთ შედეგს (FluentAssertions-ით)
            // ველოდებით 201 Created სტატუსს, რადგან POST მოთხოვნა გავუშვით
            response.StatusCode.Should().Be(HttpStatusCode.Created); 
            
            // ვამოწმებთ, რომ პასუხში ნამდვილად დაგვიბრუნდა ჩვენი გაგზავნილი Action
            response.Content.Should().Contain("ACTIVATE_ROAMING");
            
            // ბეჭდვა კონსოლში უკეთესი ხილვადობისთვის
            System.Console.WriteLine($"[Test Log]: პაკეტი წარმატებით გააქტიურდა ნომერზე: {testUser.PhoneNumber}");
        }
    }
}