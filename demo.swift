import Appwrite
import AppwriteModels

func main() async throws {
    let client = Client()
        .setEndpoint("https://cloud.appwrite.io/v1")
        .setProject("6557d0f6f0454be2134d")

    let databases = Databases(client)

    do {
        let document = try await databases.createDocument(
            databaseId: "data-tan",
            collectionId: "6558e7dfa3790fd83011",
            documentId: ID.unique(),
            data: ["title" : "hamlet"]
        )
    } catch {
        print(error.localizedDescription)
    }
}
