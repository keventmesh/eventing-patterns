# Orchestration pattern

Sequence Flows are an implementation of the Orchestration pattern, allowing an ordered execution of services or event flows. The Knative `Sequence` API simplifies the management and monitoring of event flows, making it easier to understand and debug the process

## Example

1. Run the following command to create the resources to showcase a sequence flow:
    ```shell
    $ kubectl apply -f example.yaml
    ```
2. Run the following command to send a CloudEvent to the Sequence:
    ```shell
    $ kn event send --to Sequence:flows.knative.dev/v1:sequence -f message="Hello Paris\!" -t com.foo.bar
    ```
3. View logs:
    ```shell
    $ kubectl logs -l=app=event-display -f
   
   ☁️  cloudevents.Event
      Context Attributes,
      specversion: 1.0
      type: com.foo.bar
      source: kn-event/v1.11.0
      id: 4948bceb-b04e-4ed4-ba42-a91791755236
      time: 2024-02-27T10:55:31.397575341Z
      datacontenttype: application/json
      Data,
      {
        "id": 0,
        "message": "Hello Paris! - Handled by first! - Handled by second!"
      }
    ```