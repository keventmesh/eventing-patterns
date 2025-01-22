import os
import time
import requests
from cloudevents.http import CloudEvent, to_structured
from typing import Optional, Dict, Any
import logging

class Client:
    def __init__(
        self,
        event_endpoint: str,
        status_endpoint: str,
        polling_interval: int = 5,
        max_retries: int = 100
    ):
        """
        Initialize the CloudEvent client.
        
        Args:
            event_endpoint: The endpoint to send CloudEvents to
            status_endpoint: The endpoint to poll for status
            polling_interval: Time in seconds between polling attempts
            max_retries: Maximum number of polling attempts
        """
        self.event_endpoint = event_endpoint
        self.status_endpoint = status_endpoint
        self.polling_interval = polling_interval
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

    def send_event(self, event_data: Dict[str, Any], event_type: str) -> Optional[str]:
        """
        Send a CloudEvent and handle the response.
        
        Args:
            event_data: The data to be included in the CloudEvent
            event_type: The type of the CloudEvent
            
        Returns:
            Optional[str]: The final resource URI if successful, None otherwise
        """
        # Create the CloudEvent
        attributes = {
            "type": event_type,
            "source": "http://client/client-producer",
        }
        event = CloudEvent(attributes, event_data)
        
        # Convert to structured HTTP format
        headers, body = to_structured(event)
        
        try:
            # Send the event
            response = requests.post(
                self.event_endpoint,
                headers=headers,
                data=body
            )
            
            # Check for 202 Accepted
            if response.status_code >= 200 and response.status_code < 300:
                self.logger.info("Event accepted, starting status polling")
                return self._poll_status(event['id'])
            else:
                self.logger.error(f"Unexpected response status: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending event: {e}")
            return None

    def _poll_status(self, id: str) -> Optional[str]:
        """
        Poll the status endpoint until a redirect is received.
        
        Returns:
            Optional[str]: The final resource URI if successful, None otherwise
        """
        attempts = 0
        
        while attempts < self.max_retries:
            try:

                self.logger.info(f"Polling status for event {id}")
                # Allow redirects=False to handle redirects manually
                response = requests.get(f"{self.status_endpoint}/status/{id}", allow_redirects=False)
                
                # Check for redirect status codes
                if response.status_code in (301, 302):
                    resource_uri = response.headers.get('Location')
                    if resource_uri:
                        self.logger.info(f"Received redirect to: {resource_uri}")
                        # Follow the redirect
                        final_response = requests.get(resource_uri)
                        if final_response.ok:
                            return resource_uri
                        else:
                            self.logger.error("Failed to access resource URI")
                            return None
                    
                elif response.status_code >= 500:
                    self.logger.error(f"Error response from status endpoint: {response.status_code}")
                    return None
                    
                self.logger.info(f"No redirect waiting for {self.polling_interval}")
                # If no redirect, wait and try again
                time.sleep(self.polling_interval)
                attempts += 1
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error polling status: {e}")
                return None
                
        self.logger.error("Max polling attempts reached")
        return None

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Get endpoints from environment
    event_endpoint = os.getenv('K_SINK')
    status_endpoint = os.getenv('STATUS_ENDPOINT')
    
    if not event_endpoint or not status_endpoint:
        raise ValueError("K_SINK and STATUS_ENDPOINT environment variables must be set")
    
    # Initialize client
    client = Client(event_endpoint, status_endpoint)
    
    # Example event data
    event_data = {
        "message": "Hello, World!",
        "timestamp": time.time()
    }
    
    # Send event and handle response
    resource_uri = client.send_event(event_data, "com.example.test")
    
    if resource_uri:
        print(f"Successfully processed event. Resource URI: {resource_uri}")
    else:
        print("Failed to process event")

if __name__ == "__main__":
    main()
