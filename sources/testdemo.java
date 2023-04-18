import com.microsoft.azure.cognitiveservices.search.imagesearch.*;
import com.microsoft.azure.cognitiveservices.search.imagesearch.models.*;

import java.util.List;

public class SearchImages {
    public static void main(String[] args) {
        try {
            // Set the API endpoint and key
            String endpoint = "https://api.cognitive.microsoft.com/";
            String subscriptionKey = "<your-subscription-key>";

            // Create a client
            ImageSearchAPI client = ImageSearchManager.authenticate(subscriptionKey).withEndpoint(endpoint);

            // Search for images of "Gibson Les Paul Guitars"
            Images imageResults = client.images().search("Gibson Les Paul Guitars").withMarket("en-US").withCount(10).execute().body();

            // Sort the results by price
            List<ImageObject> sortedResults = imageResults.value().stream()
                    .sorted((i1, i2) -> Double.compare(i1.price().value(), i2.price().value()))
                    .limit(10)
                    .collect(Collectors.toList());

            // Print the URLs of the top 10 results
            for (ImageObject result : sortedResults) {
                System.out.println(result.contentUrl());
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
    }
}
