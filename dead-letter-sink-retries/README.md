# Dead Letter Sink and Retries pattern

Dead letter sink are Event sinks that receive events that can't be processed successfully by
subscribers.

Dead letter sinks are useful for debugging applications because they let you isolate unconsumed
events to determine why their processing didn't succeed.

## Example

1. Run the following command to create the resources to showcase dead letter sinks and retries:
    ```shell
    $ kubectl apply -f example.yaml
    ```
2. View logs:
    ```shell
    $ kubectl logs -l=app=event-display -f
   
   ☁️  cloudevents.Event
      Context Attributes,
      specversion: 1.0
      type: dev.knative.sources.ping
      source: /apis/v1/namespaces/default/pingsources/with-dead-letter-sink
      id: f95a3409-12dc-4ed2-ba53-dbd60210e036
      time: 2024-02-15T14:26:00.115167526Z
      Extensions,
      knativearrivaltime: 2024-02-15T14:26:00.11706994Z
      knativebrokerttl: 255
      knativeerrorcode: 500
      knativeerrordata: ZGlzcGF0Y2ggZXJyb3I6IFBvc3QgImh0dHA6Ly9mYWlsLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiOiBkaWFsIHRjcDogbG9va3VwIGZhaWwuZGVmYXVsdC5zdmMuY2x1c3Rlci5sb2NhbCBvbiAxMC45Ni4wLjEwOjUzOiBubyBzdWNoIGhvc3Q=
      knativeerrordest: http://fail.default.svc.cluster.local
      Data,
      Hello World!
    ```
   Example output:
   ```shell
   ```
3. Debugging the reason using `knativeerrordata` attribute:
   ```shell
   $ echo ZGlzcGF0Y2ggZXJyb3I6IFBvc3QgImh0dHA6Ly9mYWlsLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiOiBkaWFsIHRjcDogbG9va3VwIGZhaWwuZGVmYXVsdC5zdmMuY2x1c3Rlci5sb2NhbCBvbiAxMC45Ni4wLjEwOjUzOiBubyBzdWNoIGhvc3Q= | base64 -d
   dispatch error: Post "http://fail.default.svc.cluster.local": dial tcp: lookup fail.default.svc.cluster.local on 10.96.0.10:53: no such host
   ```

