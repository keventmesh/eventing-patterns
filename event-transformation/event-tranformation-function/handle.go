package function

import (
	"context"
	"fmt"

	"github.com/cloudevents/sdk-go/v2/event"
)

type DataV1 struct {
	OrderID string `json:"orderID"`
}

type DataV2 struct {
	OrderID string `json:"order_id"`
}

func toDataV2(d DataV1) DataV2 {
	return DataV2{OrderID: d.OrderID}
}

// Handle an event.
func Handle(ctx context.Context, e event.Event) (*event.Event, error) {

	// from
	//  {
	// 	  "specversion": "1.0",
	// 	  "type": "com.example.orders.created",
	// 	  "id": "bbc79d65-1ca8-4f8c-ba77-54a1189a0e32",
	// 	  "source": "com.example.orders",
	// 	  "dataschema": "https://my-org.com/schemas/orders/v1",
	// 	  "data": {
	// 	    "orderID": "1205e9ad-132d-4291-8649-4438f4959862"
	// 	  }
	//  }
	// to
	// {
	// 	  "specversion": "1.0",
	// 	  "type": "com.example.orders.created",
	// 	  "id": "bbc79d65-1ca8-4f8c-ba77-54a1189a0e32",
	// 	  "source": "com.example.orders",
	// 	  "dataschema": "https://my-org.com/schemas/orders/v2",
	// 	  "data": {
	// 	    "order_id": "1205e9ad-132d-4291-8649-4438f4959862"
	// 	  }
	// }

	if err := e.Validate(); err != nil {
		return nil, fmt.Errorf("input event is not valid: %w", err)
	}

	data := DataV1{}
	if err := e.DataAs(&data); err != nil {
		return nil, fmt.Errorf("failed to unmarshal data into %T: %w", data, err)
	}

	e.SetDataSchema("https://my-org.com/schemas/orders/v2")

	if err := e.SetData(event.ApplicationJSON, toDataV2(data)); err != nil {
		return nil, fmt.Errorf("failed to set data: %w", err)
	}

	return &e, nil // echo to caller
}
