// uncomment below line when we are running it using "func run"
package function

// uncomment below line when we are running it in localhost, and comment out the above line
// package main

import (
	"context"
	"fmt"

	// "encoding/json"
	// "io"
	// "net/http"
	// "strings"
	"log"
	"time"

	// "bytes"
	"encoding/json"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"github.com/cloudevents/sdk-go/v2/event"
)

// init function is to be change to main, when running it 'localhost'
// func main() {

// func init() {
// 	// check ENV variables
// 	mongoURIFromEnv, exists := os.LookupEnv("MONGO_URI")
// 	var mongoURI string
// 	if exists {
// 		mongoURI = mongoURIFromEnv
// 	} else {
// 		mongoURI = defaultMongoURI
// 	}
// 	fmt.Println("MONGO_URI: "+mongoURI)

// 	emitterURLFromEnv, exists := os.LookupEnv("EMITTER_URL")
// 	var emitterURL string
// 	if exists {
// 		emitterURL = emitterURLFromEnv
// 	} else {
// 		emitterURL = defaultEmitterURL
// 	}
// 	fmt.Println("EMITTER_URL: "+emitterURL)
// 	/*
// 		The purpose of creating a context with a timeout is to associate a deadline with the request.
// 		If the request processing takes longer than the specified timeout,
// 		the context will be canceled, and any operations associated with it will be interrupted.

// 		context.Background(), which creates a background context without a timeout or deadline.
// 	*/

// 	// Start the HTTP server
// 	http.HandleFunc("/", func(res http.ResponseWriter, req *http.Request) {
// 	})

// 	// Run Handle function every 10 seconds in a goroutine (cron)

// 	go func() {
// 		ticker := time.NewTicker(10 * time.Second)
// 		defer ticker.Stop()
// 		for {
// 			select {
// 			case <-ticker.C:
// 				ctx := context.Background()
// 				e := event.New()
// 				Handle(ctx, e) // You can pass nil or mock objects here
// 			}
// 		}
// 	}()

// 	fmt.Println("Running on host port 8080")
// 	log.Fatal(http.ListenAndServe(":8080", nil))
// }

// Reminder struct represents the structure of a reminder document in the database.
type Reminder struct {
	ID        string `json:"_id,omitempty" bson:"_id,omitempty"`
	Title     string `json:"title,omitempty" bson:"title,omitempty"`
	Content   string `json:"description,omitempty" bson:"description,omitempty"`
	UserId    string `json:"user_id,omitempty" bson:"user_id,omitempty"`
	Expired   bool `json:"expired,omitempty" bson:"expired,omitempty"`
	Date      time.Time `json:"date,omitempty" bson:"date,omitempty"`
}


// MongoDB configuration
const (
	defaultMongoURI  = "mongodb://localhost:27017"
	defaultEmitterURL       = "http://localhost:5002"     
	databaseName  	 = "notes-db"
	collectionName   = "reminders"
)

// fetchDataFromDatabase fetches all documents of reminders from the MongoDB database.
func fetchDataFromDatabase() ([]*Reminder, error) {
	// Get the value of the environment variable for mongoURI, or use the default value
	mongoURIFromEnv, exists := os.LookupEnv("MONGO_URI")
	var mongoURI string
	if exists {
		mongoURI = mongoURIFromEnv
	} else {
		mongoURI = defaultMongoURI
	}
	fmt.Println("mongo uri",mongoURI)
    client, err := mongo.NewClient(options.Client().ApplyURI(mongoURI))
    if err != nil {
        log.Fatal("Error creating MongoDB client:", err)
        return nil,nil
    }

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    err = client.Connect(ctx)
    if err != nil {
        log.Fatal("Error connecting to MongoDB:", err)
		return nil,nil
    }

    defer func() {
        if err := client.Disconnect(ctx); err != nil {
            log.Fatal("Error disconnecting from MongoDB:", err)
        }
    }()

	pingErr := client.Ping(ctx, nil)
	if pingErr != nil {
		fmt.Println(pingErr.Error())
		return nil,nil
	}

    fmt.Println("Connected to MongoDB")

    // Access the reminders collection
    collection := client.Database(databaseName).Collection(collectionName)

	// Get the current time in UTC
	currentDateUTC := time.Now().UTC().Truncate(time.Minute)

	// Add 5 hours and 30 minutes to the current time in UTC, so that it matchs indian time
	currentDateUTC = currentDateUTC.Add(5*time.Hour + 30*time.Minute)

	// Calculate the next minute to include records up to the next minute
	nextMinute := currentDateUTC.Add(time.Minute)

	fmt.Printf("Current time in UTC: %v\n", currentDateUTC)
	fmt.Printf("Next minute in UTC: %v\n", nextMinute)

	// Define the filter to get all documents
	filter := bson.D{
		{"date", bson.D{
			{"$gte", currentDateUTC},
			{"$lt", nextMinute},
		}},
	}


    // Define the projection to include only specific fields in the result
    projection := bson.D{
        {"_id", 1},
        {"title", 1},
        {"description", 1},
		{"user_id", 1},
		{"expired", 1},
		{"date", 1},
    }

    // Query the database to get all reminders with the specified projection
    cursor, err := collection.Find(ctx, filter, options.Find().SetProjection(projection))
    if err != nil {
        log.Fatal("Error querying reminders collection:", err)
		return nil,nil
    }

    defer cursor.Close(ctx)

	// Create a slice to hold the fetched reminders
	var remindersList []*Reminder

    // Iterate over the cursor and print each reminder
    for cursor.Next(ctx) {
        var reminder *Reminder // Note the use of pointer here
        if err := cursor.Decode(&reminder); err != nil {
            log.Printf("Error decoding reminder document:", err)
			return nil,nil
        }
		remindersList = append(remindersList, reminder)
        fmt.Printf("Fetched Reminder: %+v\n", *reminder)
    }

    if err := cursor.Err(); err != nil {
        log.Printf("Error iterating over cursor:", err)
    }

    if len(remindersList) > 0 {
        fmt.Println("Reminders fetched.")
        return remindersList, nil
    } else {
        fmt.Println("No reminders to send.")
        return nil, nil
    }
}

// Handle an event.
func Handle(ctx context.Context, e event.Event) (*event.Event, error) {
	fmt.Println("************Processing Request*************")
	// Create a new CloudEvent instance
	newCloudEvent := event.New()

	// Fetch the data from the database

	reminders, err := fetchDataFromDatabase()
	if err != nil {
		log.Printf("Error fetching reminders: %v", err)
		// Handle the error accordingly
	} else {
		// Sample list of data

		// sampleReminders := []struct {
		// 	ID      int    `json:"id"`
		// 	Message string `json:"message"`
		// }{
		// 	{1, "Reminder 1"},
		// 	{2, "Reminder 2"},
		// 	{3, "Reminder 3"},
		// }
		// reminders := sampleReminders

		// Process the fetched reminders
		fmt.Println("Printing the Fetched Reminders: ", reminders)

		// Marshal your data to []byte
		dataBytes, err := json.Marshal(reminders)
		if err != nil {
			return nil, err
		}

		fmt.Println("Prepaing New Event")

		// Set the type and source attributes
		newCloudEvent.SetSource("processor-ce")
		newCloudEvent.SetType("Reminders")
		newCloudEvent.SetSubject("Reminder Records")
		// Set the ID as the current time
		newCloudEvent.SetID(fmt.Sprintf("%d", time.Now().Unix()))
		
		// Set the data in the CloudEvent
		newCloudEvent.SetData(event.ApplicationJSON, dataBytes)
		fmt.Println("Printing the Fetched Reminders: ", newCloudEvent) // echo to local output
		
	}
	return &newCloudEvent, nil // echo to caller

}
