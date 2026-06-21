using RestSharp;
using System.Threading.Tasks;

namespace TelcoFlow.Tests.Services
{
    public class TelecomApiService
    {
        private readonly RestClient _client;

        public TelecomApiService()
        {
            // ვიყენებთ სატესტო API-ს ბილინგის მიკროსერვისის იმიტაციისთვის
            _client = new RestClient("https://jsonplaceholder.typicode.com");
        }

        public async Task<RestResponse> ActivateRoamingPackageAsync(string phoneNumber, string packageId)
        {
            // ვუშვებთ POST მოთხოვნას
            var request = new RestRequest("/posts", Method.Post);
            
            // ვაგზავნით მონაცემებს (Payload)
            request.AddJsonBody(new
            {
                phone = phoneNumber,
                package = packageId,
                action = "ACTIVATE_ROAMING"
            });

            return await _client.ExecuteAsync(request);
        }
    }
}