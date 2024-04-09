package function

import (
	"context"
	"testing"

	"github.com/cloudevents/sdk-go/v2/event"
)

// TestHandle ensures that Handle accepts a valid CloudEvent without error.
func TestHandle(t *testing.T) {
	// Assemble

	orderID := "1205e9ad-132d-4291-8649-4438f4959862"

	e := event.New()
	e.SetID("bbc79d65-1ca8-4f8c-ba77-54a1189a0e32")
	e.SetType("com.example.orders.created")
	e.SetSource("com.example.orders")
	e.SetDataSchema("https://my-org.com/schemas/orders/v1")
	e.SetData("application/json", DataV1{OrderID: orderID})

	// Act
	echo, err := Handle(context.Background(), e)
	if err != nil {
		t.Fatal(err)
	}

	// Assert
	if echo == nil {
		t.Errorf("received nil event") // fail on nil
	}

	if err := echo.Validate(); err != nil {
		t.Errorf("event is not valid: %v", err)
	}

	data := DataV2{}
	if err := echo.DataAs(&data); err != nil {
		t.Errorf("failed to decode data into type %T: %v", data, err)
	}

	if data.OrderID != orderID {
		t.Errorf("unexepected order ID, got %q, want %q", data.OrderID, orderID)
	}
}
